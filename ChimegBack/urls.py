"""
URL configuration for ChimegBack project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers


from django.conf import settings
from django.conf.urls.static import static
from invoice import views
from invoice.views import CustomAuthToken
# from django.conf.urls import handler404

router = routers.DefaultRouter()

router.register(r'groups', views.GroupHDRViewSet)
router.register(r'products', views.InfoProductViewSet)


urlpatterns = [
    path('api/token/auth/', CustomAuthToken.as_view()),
    path('', include(router.urls)),
    path('', include('invoice.urls')),
    path('admin/', admin.site.urls),
    # path('', views.index)
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler404 = views.custom_404_view
