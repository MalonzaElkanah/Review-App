"""reviews URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib.auth.views import LogoutView
from django.conf.urls.static import static


from . import views
from . import settings

urlpatterns = [
    path('', views.index, name='index'),
    path('categories/<slug:slug>/<int:category_id>/', views.category_reviews, name='category-reviews'),
    path('business/<slug:slug>/<int:business_id>/', views.business_reviews, name='business-reviews'),

    path('admin/', admin.site.urls, name='administrator'),
    path('', include('social_django.urls', namespace='social')),
    #path('', views_main.index, name='index'),
    path('logout/', LogoutView.as_view(template_name=settings.LOGOUT_REDIRECT_URL), name='logout'),
    path('manage/', views.manage, name='manage'),
    path('update/user-details/', views.update_details, name='update-user'),
    path('check-email/', views.check_email, name='check-email'),
    
    path('login/', views.auth_login, name='login'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
