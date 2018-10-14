"""
SignalProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

from userApp import views as userviews
from storageApp import views as storageviews
from displayApp import views as displayviews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', userviews.index, name='index'),

    # === Captcha ===
    path('captcha', include('captcha.urls')),

    # === userApp ===
    path('login', auth_views.login, name='login'),
    path('logout', auth_views.logout, {'next_page': '/'}, name='logout'),
    path('signup', userviews.signup, name='signup'),
    path('home', userviews.home, name='home'),
    path('help', userviews.help, name='help'),

    # === storageApp ===
    path('storage/main', storageviews.storage_main, name='storage-main'),
    path('storage/input', storageviews.storage_input, name='storage-input'),
    path('storage/list', storageviews.storage_list, name='storage-list'),

    # === displayApp ===
    path('display/list', displayviews.display_list, name='display-list'),
    path('display/details', displayviews.display_details, name='display-details'),
    path('display/filtration', displayviews.display_filtration, name='display-filtration'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
