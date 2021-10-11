from django.contrib import admin

# Register your models here.
from .models import Category, Business, UserProfile

admin.site.register(Category)
admin.site.register(Business)
admin.site.register(UserProfile)