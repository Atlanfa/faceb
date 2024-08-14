from django.apps import AppConfig


class FacadlibConfig(AppConfig):
    name = 'facadlib'
    default_auto_field = 'django.db.models.BigAutoField'

    def ready(self):
        import facadlib.signals
    
