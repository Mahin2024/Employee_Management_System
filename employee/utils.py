from .models import Employee,Attendance,Leave,Salary
import calendar
from datetime import date
import calendar

def get_salary_data():
    today = date.today()
    year = today.year
    month = today.month
    month_days = calendar.monthrange(year, month)[1]
    salary_records = []
    

    month_name = calendar.month_name[month]

    for e in Employee.objects.all():
        present = Attendance.objects.filter(employee=e, status='present').count()
        half_day = Attendance.objects.filter(employee=e, status='half_day').count()
        paid_leave = sum(
            (l.end_date - l.start_date).days + 1
            for l in Leave.objects.filter(employee=e, status='approved', is_paid=True)
        )
        amount = present + (half_day * 0.5)
        total_days = present + (half_day * 0.5) + paid_leave
        try:
            daily_salary = float(e.role.salary) / month_days
        except (ValueError, TypeError):
            continue
        amount = present + (half_day * 0.5)
        amount=amount*daily_salary
        total_salary = round(total_days * daily_salary, 2)
        salary_records.append({
            'employee': e,
            'present': present,
            'half_day': half_day,
            'paid_leave': paid_leave,
            'total_salary': total_salary,
            'month': month,
            'year': year
        })
        Salary.objects.get_or_create(
            employee=e,
            month=month_name,
            defaults={
                'bonus':None,
                'deductions':total_salary-amount,      
                'net_salary':total_salary,
                'amount':amount,
                }
            
            )
        
      
    print(month_name,"Salary record created\n")

    return salary_records
