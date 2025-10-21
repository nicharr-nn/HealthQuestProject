from django.apps import AppConfig

class RecipesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'recipe'

    def ready(self):
        # ensure signals are registered
        from . import signals  # noqa: F401
        
