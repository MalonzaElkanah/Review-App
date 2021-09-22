from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from business.models import Category, Business, Review, UserProfile
from business.forms import UserProfileForm

# Create your views here.
# import google.oauth2.credentials
# import google_auth_oauthlib.flow


def index(request):
	return render(request, 'reviews/index.html')
	

def login(request):
	return render(request, 'reviews/users.html')

# Manage User-logins
def manage(request):
	# Check if user has logged In for the first time
	try:
		# Update OBJECT
		profile = UserProfile.objects.get(user=int(request.user.id))
		return redirect('index')
	except ObjectDoesNotExist:
		# Create Default Values
		profile = UserProfile(user=request.user, language='English')
		profile.save()
		# Redirect to Updating user data if object does-not exist
		return redirect('update-user')

def update_details(request):
	# Get profile details
	profile = UserProfile.objects.get(user=int(request.user.id))
	if request.method == 'POST':
		form = UserProfileForm(request.POST, request.FILES, instance=profile)
		if form.is_valid():
			form.save()
		else:
			return HttpResponse(form.errors)
		user = request.user
		user.username = request.POST['name']
		user.email = request.POST['email']
		user.save()
		return redirect('update-user')
	else:
		form = UserProfileForm(instance=profile)
		return render(request, 'reviews/profile-settings.html', {'profile': profile, 'form': form})


def category_reviews(request):
	return render(request, 'reviews/category-reviews.html')

def business_reviews(request):
	return render(request, 'reviews/business-reviews.html')