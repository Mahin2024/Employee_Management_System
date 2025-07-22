from apscheduler.schedulers.background import BackgroundScheduler
from employee.models import Employee, Attendance,Leave
from datetime import date
import calendar
    
def create_daily_attendance():
    today = date.today()
    weekday = today.weekday() 
    for employee in Employee.objects.all():
        if weekday in [5, 6]:  # 5 = Saturday, 6 = Sunday
            status = 'weekend'
        else:
            status = 'absent'
        Attendance.objects.get_or_create(
            employee=employee,
            date=today,
            defaults={
                'checkin': None,
                'is_late': False,
                'status': status,
                'location': '',  # optional
            }
        )
    print("Daily attendance entries created")


def calculate_salary():

    today = date.today()
    year = today.year
    month = today.month

    # Get number of days in the current month
    month_days = calendar.monthrange(year, month)[1]
    employee = Employee.objects.all()
    for e in employee:
        fullday = Attendance.objects.filter(employee_id=e.id,status='present').count()
        halfday_count = Attendance.objects.filter(employee_id=e.id,status='half_day').count()
        halfday_count*=0.5
        total=fullday+halfday_count
        # print(total,"total")
        paidleave = Leave.objects.filter(employee_id=e.id,status='approved',is_paid=True)
        # print(paidleave,'paidleave')
        sum=0
        for l in paidleave:
            start = l.start_date.day
            end = l.end_date.day
            sum += (end - start + 1)
        # print(sum,"paid leave sum")
        totaldays = total+sum
        # print("total days",totaldays)

        sal= e.role.salary
        # print(e)
        # print(sal)
        print("\n")
        try:
            daily_salary = float(sal) / month_days
            # print(daily_salary)
        except (TypeError, ValueError):
            print(f"Invalid salary for {e.name}: {sal}")
            continue
      
        total_salary = totaldays * daily_salary

        print(f"Total salary for {calendar.month_name[month]} {year}: ₹{total_salary}")

calculate_salary()


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(create_daily_attendance, 'cron', hour=10, minute=49)
    scheduler.add_job(calculate_salary, 'cron', day='last', hour=18, minute=0)
    scheduler.start()

