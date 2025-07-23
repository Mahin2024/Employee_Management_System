from .models import Employee,Attendance,Leave
import calendar
from datetime import date


def get_salary_data():
    today = date.today()
    year = today.year
    month = today.month
    month_days = calendar.monthrange(year, month)[1]
    salary_records = []

    for e in Employee.objects.all():
        present = Attendance.objects.filter(employee=e, status='present').count()
        half_day = Attendance.objects.filter(employee=e, status='half_day').count()
        paid_leave = sum(
            (l.end_date - l.start_date).days + 1
            for l in Leave.objects.filter(employee=e, status='approved', is_paid=True)
        )
        total_days = present + (half_day * 0.5) + paid_leave
        try:
            daily_salary = float(e.role.salary) / month_days
        except (ValueError, TypeError):
            continue
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

    return salary_records
