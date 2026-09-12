"""
Root URL configuration for the portfolio project.
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    # django-allauth handles /accounts/login/, /accounts/logout/,
    # /accounts/google/login/, and the OAuth callback at
    # /accounts/google/login/callback/
    path("accounts/", include("allauth.urls")),
    path("", include("main.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
