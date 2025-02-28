from django.apps import AppConfig


class CartConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cart'

    def ready(self):   #this ensures that signal handlers in signals.py are imported and executed when the app starts
        import cart.signals

