from apscheduler.schedulers.background import BackgroundScheduler
from employee.models import Employee, Attendance,Leave
from datetime import date
import calendar
import stripe
from django.conf import settings
from .utils import get_salary_data
    
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

stripe.api_key = settings.STRIPE_SECRET_KEY  # your test key

def simulate_stripe_salary_payment(employee, amount):
    try:
        payment_intent = stripe.PaymentIntent.create(
            amount=int(amount * 100),  # Convert ₹ to paise
            currency='inr',
            payment_method_types=["card"],
            description=f"Test Salary Payment for {employee.name}"
        )
        print(f"[STRIPE] PaymentIntent created for {employee.name}: ₹{amount}")
        print(f"→ PaymentIntent ID: {payment_intent.id}")
    except Exception as e:
        print(f"[ERROR] Stripe payment failed for {employee.name}: {e}")

def calculate_salary():
    records = get_salary_data()
    for r in records:
        simulate_stripe_salary_payment(r['employee'], r['total_salary'])
        print(f"→ Total salary for {r['employee'].name}: ₹{r['total_salary']}\n")


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(create_daily_attendance, 'cron', hour=8, minute=0)
    scheduler.add_job(calculate_salary, 'cron',day ='last', hour=20, minute=0)
    scheduler.start()