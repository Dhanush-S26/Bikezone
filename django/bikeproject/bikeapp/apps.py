from django.apps import AppConfig


class BikeappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bikeapp'
    def ready(self):
        # Import signals so they are registered
        import bikeapp.signals   # noqa: F401
