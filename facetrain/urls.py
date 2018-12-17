"""facetrain URL Configuration
"""

from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework.documentation import include_docs_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('face/', include('train.urls')),
    path('docs/', include_docs_urls(title="后台接口")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
