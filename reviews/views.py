from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from business.models import Category, Business, Review, UserProfile
from business.forms import UserProfileForm
from . import settings

# Create your views here.
from validate_email import validate_email

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

def check_email(request):
	if request.method == 'GET':
		# Get the user email
		email = request.GET['email']
		# Check if user exists
		users = User.objects.filter(email='elkanahmalonza@gmail.com')
		if users < 1:
			# New User
			# Check if the email exist
			email_status = validate_new_email(email)
			if email_status:
				# Email Exist
				pass
			else:
				# Email does not exist
				pass

			return JsonResponse({"success": "New User Sign-up: "+email})
		else:
			# User Already Exists
			pass

	else:
		return JsonResponse({"success": "GET"})

def validate_new_email(email):
	is_valid = validate_email(
		email_address=email,
		check_format=True,
		check_blacklist=True,
		check_dns=True,
		dns_timeout=10,
		check_smtp=True,
		smtp_timeout=10,
		smtp_helo_host=settings.SMTP_HOST,
		smtp_from_address=settings.SMTP_ADDRESS,
		smtp_skip_tls=False,
		smtp_tls_context=None,
		smtp_debug=False
	)
	return is_valid


def category_reviews(request):
	return render(request, 'reviews/category-reviews.html')

def business_reviews(request):
	return render(request, 'reviews/business-reviews.html')