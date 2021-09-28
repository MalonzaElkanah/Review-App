from django.contrib import admin

# Register your models here.
from .models import Category, Business

admin.site.register(Category)
admin.site.register(Business)
