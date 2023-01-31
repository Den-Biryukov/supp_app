import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'supp_app_drf_v2.settings')

application = get_asgi_application()
