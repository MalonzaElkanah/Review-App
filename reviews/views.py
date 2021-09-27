from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from business.models import Category, Business, Review, UserProfile, Confirm_Email
from business.forms import UserProfileForm
from . import settings

# Create your views here.
from validate_email import validate_email
import random

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
		if int(request.GET['step']) == 0:
			# Get the user email
			email = request.GET['email']
			# Check if user exists
			users = User.objects.filter(email=email)
			if users.count() < 1:
				# New User
				# Check if the email exist
				is_valid = validate_email(email_address=email,
				    check_format=True,
				    check_blacklist=True,
				    check_dns=True,
				    dns_timeout=10,
				    check_smtp=True,
				    smtp_timeout=10,
				    smtp_helo_host=None,
				    smtp_from_address=None,
				    smtp_skip_tls=False,
				    smtp_tls_context=None,
				    smtp_debug=False
				)
				if is_valid:
					# Email Exist
					return JsonResponse({"success": "New User, Email Passed validation test:"+email})
				else:
					# Email does not exist
					return JsonResponse({"error": "Their is issue with your email: "+email})
			else:
				# User Already Exists
				return JsonResponse({"success": "Email Aready Exists "+email})
		elif int(request.GET['step']) == 1:
			# Get the user email and name
			email = request.GET['email']
			name = request.GET['name']
			# Generate random Number between 0000 to 9999
			confirmation_code = format(random.randint(0000,9999), '04d')
			# Save random number for later varification
			data = Confirm_Email(email=email, code=confirmation_code, name=name)
			data.save()
			# Send the Code to User Email
			
			# Return Success
			return JsonResponse({"success": "Wait for Confirm Code in Your Email."})
		elif int(request.GET['step'] == 2):
			# Get User Data
			email = request.GET['email']
			name = request.GET['name']
			code = request.GET['code']
			data = Confirm_Email.objects.filter(email=email, name=name, code=code)
			if data > 0:
				# Create user by adding username(email), email and password Parameters
				user = User.objects.create_user(email, email, code)
				# Check if user has been created
				if user.is_active:
					# Add first name and last name to User object.  
					user.first_name = name
					user.save()
					# Login User
					user = authenticate(username=email, password=code)
					# Login the user if username and password is correct.
					if user is not None:
						login(request, user)
						# Delete Data from Confirm Email
						data.delete()
						# Redirect the user to the link require login
						return JsonResponse({"success": "Sign Up Succeful."})
			else:
				# Error
				return JsonResponse({"error": "Wrong Error Code"})

		else:
			return JsonResponse({"error": "Application error: "})
	else:
		return JsonResponse({"success": "GET"})

def validate_new_email(email):
	is_valid = validate_email(email, verify=True)
	return is_valid


def category_reviews(request):
	return render(request, 'reviews/category-reviews.html')

def business_reviews(request):
	return render(request, 'reviews/business-reviews.html')