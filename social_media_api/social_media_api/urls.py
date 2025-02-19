from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path("posts/", include("posts.urls")),
    path('', include('accounts.urls')),
    path('', include('posts.urls')),
    path('', include('notifications.urls')),
    path('api-auth/', include('rest_framework.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler404 = 'accounts.views.handler404'
