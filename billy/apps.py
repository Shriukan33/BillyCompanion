from django.apps import AppConfig


class BillyConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "billy"

    def ready(self):
        import billy.signals  # noqa
