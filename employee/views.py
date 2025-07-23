from datetime import datetime, timedelta
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView 
from core.permissions import ProfileIsAuthenticated
from core.authentication import encode_token
from .models import Employee,Attendance,Leave
from .serializers import loginSerializer,employeeSerializar,leaveSerializer, leaveStatusSerializer, paidLeaveSerializer
from django.contrib.auth.hashers import check_password,make_password
from rest_framework.response import Response
from rest_framework import status
import random
from django.core.mail import send_mail
from django.conf import settings
import jwt
from django.utils.timezone import now,timedelta
from geopy.distance import geodesic
from rest_framework.exceptions import ValidationError
from master.models import LeavePolicy
from django.shortcuts import render
from .utils import get_salary_data
import calendar


class loginViewset(ModelViewSet):
    http_method_names = ['post']
    serializer_class = loginSerializer

    def create(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        token = encode_token(email,password,Employee)
        office_loc = (26.90851971964874, 75.78250458115853)  

        if token.status_code == 201:

            lat = request.data.get('lat')
            lng = request.data.get('lng')
            
            emp_loc = (float(lat), float(lng))
            
            distance_m = geodesic(office_loc, emp_loc).meters
            print(f"Distance: {distance_m:.2f} meters")
            if distance_m<50:
                location = 'WFO'
            else:
                location = 'WFH'
            today = now().date()
            time = (now() + timedelta(hours=5, minutes=30)).time()
            employee=Employee.objects.filter(email=email).first()
            
            role_time = employee.role.entry
            role_datetime = datetime.combine(today, role_time) 
            role_time_plus_15 = (role_datetime + timedelta(minutes=15)).time()

            is_late = time > role_time_plus_15
            buffer_time= (role_datetime - timedelta(minutes=15)).time()

            print(buffer_time," buffer time")
            print(time," time")

            if time<buffer_time:
                return Response({"message": "You have login successfully. Attendance can only be marked after the 8:45 AM.",
                                 "token":token.data.get("token")},status=status.HTTP_200_OK)
            

            attendance = Attendance.objects.filter(employee=employee, date=today).first()

            if attendance:
                attendance.checkin = time.strftime("%H:%M:%S")
                attendance.is_late = is_late
                attendance.location = location
                attendance.save()

                # Late count for current month
                late_count = Attendance.objects.filter(
                    employee=employee,
                    is_late=True,
                    date__month=today.month,
                    date__year=today.year,
                 
                ).count()

                print(late_count,'late_count')
                email_id = employee.team_leader.email
                print(email_id, "Team leader email")

                month_name = datetime.now().strftime("%B")


                if late_count >= 3 and attendance.date==today and attendance.is_late==True:
                    send_mail(
                        subject="Regarding Late Attendance",
                        message=(
                            f"Your employee {employee} from {employee.department} department, "
                            f"working as a {employee.role}, has been late {late_count} times in {month_name}."
                        ),
                        from_email=settings.EMAIL_HOST_USER,
                        recipient_list=[email_id],
                        fail_silently=False,
                    )

                return Response({
                    "message": "Attendance updated successfully.","token": token.data.get("token"),
                    "information":{"name":employee.name,"contact_number":employee.contact,
                                   'checkin-time': time.strftime("%H:%M:%S"),'is_late': is_late,
                                    "date":today,'location':location}},status=status.HTTP_200_OK)   
                

            else:
                return Response({
                    "message": "Attendance record not found. Please contact Admin.",
                    "token": token.data.get("token"),
                }, status=status.HTTP_200_OK)  

        else:
            return Response(token.data,status=status.HTTP_400_BAD_REQUEST)
        

class logout(APIView):
    permission_classes =[ProfileIsAuthenticated] 

    def post(self,request):
        office_loc = (26.90851971964874, 75.78250458115853) 
        lat = request.data.get('lat')
        lng = request.data.get('lng')
        
        emp_loc = (float(lat), float(lng))
        
        distance_m = geodesic(office_loc, emp_loc).meters
        print(f"Distance: {distance_m:.2f} meters")
        if distance_m<50:
            location = 'WFO'
        else:
            location = 'WFH'

        today = now().date()
        
        employee = Employee.objects.get(id = request.id)
        attendance= Attendance.objects.filter(employee=employee,date =today).last()
        print(attendance)
        if attendance.location!=location:
            return Response({"message":"You have logged out successfully, but your attendance was not "
            "updated due to a location mismatch. Please contact HR to update your attendance."})
        
        checkout = (now() + timedelta(hours=5, minutes=30)).time()
        attendance.checkout=checkout
        
        role_datetime = datetime.combine(today, employee.role.exit)
        buffer_time= (role_datetime - timedelta(minutes=15)).time()

        is_early= checkout<buffer_time
        attendance.is_early=is_early

        checkin_datetime = datetime.combine(today, attendance.checkin)
        checkout_datetime = datetime.combine(today, checkout)
        duration = checkout_datetime - checkin_datetime
        
        if duration < timedelta(hours=3.5):
            attendance.status = 'absent'
        elif timedelta(hours=3.5) <= duration <= timedelta(hours=7.5):
            attendance.status = 'half_day'
        else:
            attendance.status = 'present'

        attendance.save()

        return Response({"message": "You have logout","profile": {
                    "employee": attendance.employee.name,
                    "date": str(attendance.date),
                    "checkout": attendance.checkout.strftime("%H:%M:%S") if attendance.checkout else None,
                    "is_early": attendance.is_early
                }},status=status.HTTP_200_OK)
        

class employeeViewset(ModelViewSet):
    http_method_names = ['get','patch']
    serializer_class = employeeSerializar
    permission_classes =[ProfileIsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        profile = Employee.objects.filter(id = user.id)
        print(profile)
        return profile
    
    # def partial_update(self, request, *args, **kwargs):
    #     user = self.request.user
    #     record = Employee.objects.get(id=user.id)
    #     serializer = employeeSerializar(record, data=request.data, partial=True)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class changePassword(APIView):
    permission_classes =[ProfileIsAuthenticated]
    def post(self, request):
        user = request.user
        data = request.data

        old_password = data.get('old_password')
        new_password = data.get('new_password')
        confirm_password = data.get('confirm_password')

        if not old_password or not new_password or not confirm_password:
            return Response({"message": "All password fields are required."}, status=status.HTTP_400_BAD_REQUEST)

        if not check_password(old_password, user.password):
            return Response({"message": "Old password is incorrect."}, status=status.HTTP_400_BAD_REQUEST)

        if new_password != confirm_password:
            return Response({"message": "New passwords do not match."}, status=status.HTTP_400_BAD_REQUEST)

        user.password = make_password(new_password)
        user.save()

        return Response({"message": "Password updated successfully."}, status=status.HTTP_200_OK)
    

class forgotPassword(APIView):
    # permission_classes =[ProfileIsAuthenticated]
    def post(self, request):
        otp = random.randint(1000,9999)
        data = request.data
        email = data.get('email')
        secret = "secret_key"

        send_mail(
            subject='Password forgot OTP',
            message=f'Your OTP is: {otp}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list= [email],
            fail_silently=False,
            )
        
        user = Employee.objects.filter(email=email).first()
        user_id = user.id
        encrypt_otp = make_password(str(otp)) 
        encoded = jwt.encode({"otp":encrypt_otp, "id":user_id},secret, algorithm="HS256")
        print("token : ", encoded)
        # print("Encrypt OTP : ", encrypt_otp)
        return Response({"token":encoded},status=status.HTTP_201_CREATED)


class resetPassword(APIView):
    
    def post(self,request):
        secret = "secret_key"
        token = request.data.get('token')

        if not token:
            return Response({"error":"Token is required"},status=status.HTTP_400_BAD_REQUEST)
        try:
            decoded = jwt.decode(token, secret, algorithms="HS256")
            user_id = decoded.get('id')
            hash_otp = decoded.get('otp')

            user = Employee.objects.filter(id=user_id).first()
            data = request.data
        
            otp = data.get('otp')
            new_password = data.get('new_password')
            confirm_password = data.get('confirm_password')

            if " " in new_password:
                return Response({"message": "space not excepted in password"}, status=status.HTTP_400_BAD_REQUEST)

            if not otp or not new_password or not confirm_password:
                return Response({"message": "All fields are required."}, status=status.HTTP_400_BAD_REQUEST)

            if not check_password(otp, hash_otp):
                return Response({"message": "OTP is incurrect"}, status=status.HTTP_400_BAD_REQUEST)

            if new_password != confirm_password:
                return Response({"message": "New passwords do not match."}, status=status.HTTP_400_BAD_REQUEST)

            user.password = make_password(new_password)
            user.save()

            return Response({"message": "Password Reset successfully."}, status=status.HTTP_200_OK)
        except Exception as e:
            print("token change")
            return Response({"error":str(e)},status=status.HTTP_400_BAD_REQUEST)
        

class leaveViewset(ModelViewSet):
    http_method_names = ['post','get']
    queryset=Leave.objects.all()
    serializer_class = leaveSerializer
    permission_classes =[ProfileIsAuthenticated]

    def perform_create(self, serializer):
        employee = Employee.objects.get(id=self.request.user.id)
        start_date=self.request.data.get('start_date')
        end_date=self.request.data.get('end_date')
        today = str(now().date())
        type = self.request.data.get('type')
        policy=self.request.data.get('policies')
        if end_date<start_date or start_date<today:
            raise ValidationError("Start date must be today or later, and end date must be the same or after start date.")
        
        if type == 'half_day':
            if end_date!=start_date:
                raise ValidationError("Start date must be end date")
            
            
        leave = Leave.objects.filter(policies_id=policy,employee=employee,status='approved',is_paid=True)
        print(leave)
        sum = 0
        for l in leave:

            if l.type == 'half_day':
                sum = sum + 0.5
            else: 
                start = l.start_date.day
                end = l.end_date.day
                sum += (end - start + 1)

        print(sum,"paid leave sum")
        id = self.request.data.get('policies')
        total_leave=LeavePolicy.objects.filter(id=id).first().leave_count

        print(total_leave)

        if sum<=float(total_leave):
            is_paid =True
        else:
            is_paid =False

        serializer.save(employee=employee,is_paid=is_paid)

class leaveStatusViewset(ModelViewSet):
    http_method_names=['get','patch']
    serializer_class=leaveStatusSerializer
    permission_classes=[ProfileIsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        employee= Leave.objects.filter(employee__team_leader=user.id,status='pending')
        print(employee)
        return employee
    
class paidLeaveViewset(APIView):
    permission_classes = [ProfileIsAuthenticated]

    def get(self, request):
        user=self.request.user
        leave=Leave.objects.filter(employee_id=user.id,status='approved',is_paid=True)
        print(leave)
         
        take_leave = 0
        paid=0
        sick=0
        casual=0
        
        for l in leave:

            if l.type == 'half_day':
                take_leave= 0.5
            else: 
                start = l.start_date.day
                end = l.end_date.day
                take_leave = (end - start + 1)

            if l.policies.type == 'Paid':
                paid += take_leave
            elif l.policies.type == 'Casual':
                casual += take_leave
            elif l.policies.type == 'Sick':
                sick += take_leave

        print("Used Leaves",{"sick leave": sick, "casual leave": casual, "paid leave": paid})

        sick_policy = LeavePolicy.objects.get(type='Sick')
        casual_policy = LeavePolicy.objects.get(type='Casual')
        paid_policy = LeavePolicy.objects.get(type='Paid')

        sick_leave = float(sick_policy.leave_count) - float(sick)
        casual_leave = float(casual_policy.leave_count) - float(casual)
        paid_leave = float(paid_policy.leave_count) - float(paid)

        if sick_leave<0:
            sick_leave=0
        if casual_leave<0:
            casual_leave=0
        if paid_leave<0:
            paid_leave=0
        return  Response({"sick leave": sick_leave, "casual leave": casual_leave, "paid leave": paid_leave})
    

def salary_view(request):
    salary_records = get_salary_data()
    if salary_records:
        month = calendar.month_name[salary_records[0]['month']]
        year = salary_records[0]['year']
    else:
        month = ''
        year = ''
    return render(request, 'salary_template.html', {
        'salary_records': salary_records,
        'month': month,
        'year': year
    })
     