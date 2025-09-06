# rethread/apps.py

from django.apps import AppConfig

class RethreadConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'rethread'

    def ready(self):
        from . import signals