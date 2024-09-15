from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from journalist.api import ArticleViewSet
from django.conf import settings
from django.conf.urls.static import static
from users.views import *

router = DefaultRouter()
router.register(r'articles', ArticleViewSet)

urlpatterns = [
    path('',login_view,name='login'),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('journalist/', include('journalist.urls')),
    path('editor/', include('editor.urls')),
    path('head/', include('head.urls')),
    path('api/', include(router.urls)),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)