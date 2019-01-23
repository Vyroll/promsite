from django.apps import AppConfig


class BlogdemoConfig(AppConfig):
    name = 'blogdemo'

    def ready(self):
        import blogdemo.signals