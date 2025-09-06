import sys
import os
import django

sys.path.append('C:/Users/Chaithra R/') 

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecofinds.settings')
django.setup()


from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent

INSTALLED_APPS = [
    "django.contrib.admin", "django.contrib.auth", "django.contrib.contenttypes",
    "django.contrib.sessions", "django.contrib.messages", "django.contrib.staticfiles",
    "rethread", "ecofinds", # <-- our app
]

#Static & Media
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]  # create this folder next
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"           # uploaded images live here

#Templates (APP_DIRS=True lets Django auto-discover marketplace/templates)
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],  
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

#Auth convenience
LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "product_list"
LOGOUT_REDIRECT_URL = "product_list"
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("ecofinds.urls")),  # our app routes
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

