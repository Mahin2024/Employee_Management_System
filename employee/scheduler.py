from apscheduler.schedulers.background import BackgroundScheduler
from employee.models import Employee, Attendance
from datetime import date
    
    
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

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(create_daily_attendance, 'cron', hour=10, minute=49)
    scheduler.start()

