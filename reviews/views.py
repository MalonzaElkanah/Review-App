from django.shortcuts import render

# Create your views here.


def index(request):
	return render(request, 'reviews/index.html')

def login(request):
	return render(request, 'reviews/users.html')

def category_reviews(request):
	return render(request, 'reviews/category-reviews.html')

def business_reviews(request):
	return render(request, 'reviews/business-reviews.html')