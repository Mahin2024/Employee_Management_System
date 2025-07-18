from django.apps import AppConfig


class EmployeeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'employee'

    def ready(self):
        import employee.signals  # if you're using signals
        from employee import scheduler
        scheduler.start()
