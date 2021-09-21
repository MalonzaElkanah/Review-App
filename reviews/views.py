from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from business.models import Category, Business, Review

# Create your views here.
# import google.oauth2.credentials
# import google_auth_oauthlib.flow


def index(request):
	return render(request, 'reviews/index.html')
	

def login(request):
	return render(request, 'reviews/users.html')


def manage(request):
    return render(request, 'reviews/manage.html')


def category_reviews(request):
	return render(request, 'reviews/category-reviews.html')

def business_reviews(request):
	return render(request, 'reviews/business-reviews.html')