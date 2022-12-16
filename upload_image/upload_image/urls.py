"""upload_image URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from upload_app import views




urlpatterns = [
    path('admin/', admin.site.urls),
    path('home',views.home, name="home"),
    path('login/',views.login_user, name="login"),
    path('signup_ajax',views.signup, name="signup_ajax"),
    path('get_url_to_talk',views.get_url_to_talk, name="get_url_to_talk"),
    
    path('pro/<str:groupname>/',views.index, name="index"),


] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
