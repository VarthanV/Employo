from django.apps import AppConfig


class EmployoappConfig(AppConfig):
    name = 'employoapp'
    def ready(self):
        import employoapp.signals
        

