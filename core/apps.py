import threading
from django.apps import AppConfig
from django.core.cache import cache


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        import core.signals

        # def initialize_class():
        #     from .img_filter import ImageFilter
        #     filter_model = ImageFilter()
        #     cache.set('filter_model', filter_model, timeout=None)
        #
        # threading.Thread(target=initialize_class, daemon=True).start()
