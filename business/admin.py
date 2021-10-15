from django.contrib import admin

# Register your models here.
from .models import Category, Business, UserProfile, EmailApp

admin.site.register(Category)
admin.site.register(Business)
admin.site.register(UserProfile)
admin.site.register(EmailApp)