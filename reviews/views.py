from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail, BadHeaderError
from django.template.loader import render_to_string

from business.models import Category, Business, Review, UserProfile, Confirm_Email
from business.forms import UserProfileForm
from . import settings

# Create your views here.
from validate_email import validate_email
import random

def index(request):
	categories = Category.objects.all()
	return render(request, 'reviews/index.html', {'categories': categories})


def category_reviews(request, slug, category_id):
	category = Category.objects.get(id = int(category_id))
	categories = Category.objects.all()
	return render(request, 'reviews/category-reviews.html', {"category": category, 
		'categories': categories})


def business_reviews(request, slug, business_id):
	business = Business.objects.get(id=int(business_id))
	return render(request, 'reviews/business-reviews.html', {'business': business})


def auth_login(request):
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
					return JsonResponse({"success": "Enter Your name to Continue."})
				else:
					# Email does not exist
					return JsonResponse({"error": "Their is issue with your Email address."})
			else:
				# User Already Exists
				user = users[0]
				if send_code_email(user.email, user.first_name):
					return JsonResponse({"success": "Code will be send to "+email, 
						"user_name": user.first_name})
				else:
					return JsonResponse({"error": "Error Occured in sending Email"})
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
			subject = "Use code " + confirmation_code + " to set up your BizReviews account"
			email_template_name = "email/confirmation_code_new_user.txt"
			c = {
				"email": email,
				'name': name,
				'code': confirmation_code,
			}
			email_body = render_to_string(email_template_name, c)
			try:
				send_mail(subject, email_body, 'admin@example.com' , [email], fail_silently=False)
			except BadHeaderError:
				return JsonResponse({"error": "Invalid Header Found."})
			# Return Success
			return JsonResponse({"success": "Wait for Confirm Code in Your Email."})
		elif int(request.GET['step']) == 2:
			# Get User Data
			email = request.GET['email']
			name = request.GET['name']
			code = request.GET['code']
			# Check if user is new
			users = User.objects.filter(email=email)
			data = Confirm_Email.objects.filter(email=email, name=name, code=code)
			if data.count() > 0:
				user = None
				if users.count() < 1:
					# Create user by adding username(email), email and password Parameters
					user = User.objects.create_user(email, email, code)
				else:
					user = users[0]
				# Check if user has been created
				if user.is_active:
					if users.count() < 1:
						# Add first name and last name to User object.  
						user.first_name = name
						user.save()
					else:
						user.set_password(code)
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
						return JsonResponse({"error": "Password Error"})

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



def send_code_email(email, name):
	# Generate random Number between 0000 to 9999
	confirmation_code = format(random.randint(0000,9999), '04d')
	# Save random number for later varification
	data = Confirm_Email(email=email, code=confirmation_code, name=name)
	data.save()
	# Send the Code to User Email
	subject = "Use code " + confirmation_code + " to set up your BizReviews account"
	email_template_name = "email/confirmation_code_new_user.txt"
	c = {
		"email": email,
		'name': name,
		'code': confirmation_code,
	}
	email_body = render_to_string(email_template_name, c)
	try:
		send_mail(subject, email_body, 'admin@example.com' , [email], fail_silently=False)
	except BadHeaderError:
		return False
	return True