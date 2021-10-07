from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail, BadHeaderError
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.text import slugify

from business.models import Category, Business, Review, UserProfile, Confirm_Email
from business.forms import UserProfileForm
from . import settings

# Create your views here.
from validate_email import validate_email
import random


def check_user_settings(user):
	profile = UserProfile.objects.filter(user=user.id)
	return profile.count()>=1


def index(request):
	# Get Category and Review Data
	categories = Category.objects.all()
	all_reviews = Review.objects.all()
	reverse_reviews = all_reviews.order_by('date_created').reverse().distinct()
	# Initiate Slider Reviews Variable
	reviews1 = None
	reviews2 = None
	reviews3 = None
	# Check if their is enough review to populate all homepage slider
	if reverse_reviews.count() >= 15:
		# If more than 14 reviews populate all 3 review slider
		reviews1 = reverse_reviews[0:5]
		reviews2 = reverse_reviews[5:10]
		reviews3 = reverse_reviews[10:15]
	elif reverse_reviews.count() >= 10:
		# If more than 9 reviews populate only 2 review slider 
		reviews1 = reverse_reviews[0:5]
		reviews2 = reverse_reviews[5:10]
	elif reverse_reviews.count() >= 5: 
		# If more than 4 reviews populate only 1 review slider 
		# Their will be no sliding animation
		reviews1 = reverse_reviews[0:5]
	else:
		# If less than 4 reviews populate only 1 review slider
		# Their will be no sliding animation
		reviews1 = reverse_reviews
		
	reviews = [reviews1, reviews2, reviews3]
	return render(request, 'reviews/index.html', {'categories': categories, 'reviews': reviews})


def category_reviews(request, slug, category_id):
	category = Category.objects.get(id = int(category_id))
	categories = Category.objects.all()
	return render(request, 'reviews/category-reviews.html', {"category": category, 
		'categories': categories})


def business_reviews(request, slug, business_id):
	business = Business.objects.get(id=int(business_id))
	return render(request, 'reviews/business-reviews.html', {'business': business})


def profile_reviews(request, slug, user_id):
	profile = UserProfile.objects.get(id=int(user_id))
	return render(request, 'reviews/profile-reviews.html', {'profile': profile})


@login_required(login_url='/login/')
def review_business(request, slug, business_id):
	business = Business.objects.get(id=int(business_id))
	if request.is_ajax():
		# Get Data: business, user, rating, title, review
		rate = request.GET['rate']
		review = request.GET['review']
		title = request.GET['title']
		# Add Rating 
		new_review = Review(business=business, user=request.user, rating=rate, title=title, 
			review=review)
		new_review.save()
		# Redirect Url
		url = 'review/' + slugify(title) + '/' + str(new_review.id) + '/'
		# Ajax Response
		return JsonResponse({"success": "Review Submitted.", "redirect": "../../../"+url})
	else:
		# GET Data if any
		rate = int(request.GET.get('rate', 0))
		
		return render(request, 'reviews/review-business.html', {'business': business, 'rate': rate})


@login_required(login_url='/login/')
@user_passes_test(check_user_settings, login_url='/manage/')
def my_reviews(request):
	reviews = Review.objects.filter(user=request.user.id)
	profile = UserProfile.objects.get(user=int(request.user.id))
	return render(request, "reviews/my-reviews.html", {"reviews": reviews, "profile": profile})


@login_required(login_url='/login/')
@user_passes_test(check_user_settings, login_url='/manage/')
def my_review(request, slug, review_id):
	reviews = Review.objects.filter(id=int(review_id))
	review = None
	if reviews.count() > 0:
		review = reviews[0]
	profile = UserProfile.objects.get(user=int(request.user.id))
	return render(request, "reviews/my-review.html", {"review": review, "profile": profile})


@login_required(login_url='/login/')
@user_passes_test(check_user_settings, login_url='/manage/')
def edit_review(request, slug, review_id):
	# Get the User Review to be editted
	reviews = Review.objects.filter(id=int(review_id), user=request.user.id)
	review = None
	# Check if Review Exist
	if reviews.count() > 0:
		# Review Exist
		review = reviews[0]
		# Check if request is AJAX
		if request.is_ajax():
			# Get Data: business, user, rating, title, review, id
			rate = request.GET['rate']
			user_review = request.GET['review']
			title = request.GET['title']
			ajax_review_id = int(request.GET['id'])
			# Update Review if ID match
			if ajax_review_id == review.id: 
				# Update Review
				review.title = title
				review.rating = rate
				review.review = user_review
				review.save()
				# Redirect Url
				url = 'review/' + slugify(title) + '/' + str(review.id) + '/'
				# Ajax Succeful Response
				return JsonResponse({"success": "Review Updated.", "redirect": "../../../../"+url})
			else:
				# Ajax Failure Response
				return JsonResponse({"error": "An Error Occured. Refresh the page and Try Again."})
		else:
			# if Request is not AJAX return a HTML VIEW to edit the Review
			return render(request, "reviews/edit-review.html", {"review": review})
	else:
		return HttpResponse("Access Denied: <a href='../../../'>Back home</a>")


@login_required(login_url='/login/')
@user_passes_test(check_user_settings, login_url='/manage/')
def delete_review(request, slug, review_id):
	# Check if request is AJAX
	if request.is_ajax():
		reviews = Review.objects.filter(id=int(review_id), user=request.user.id)
		review = None
		if reviews.count() > 0:
			review = reviews[0]
			reviews.delete()
			url = 'my-reviews/'
			# Ajax Succeful Response
			return JsonResponse({"success": "Review Deleted.", "redirect": "../../../../"+url})
		else:
			# Ajax Failure Response
			return JsonResponse({"error": "Access Denied."})
	else:
		return HttpResponse("An Error Occured. Please Try Again Later.")



def auth_login(request):
	return render(request, 'reviews/users.html')


@login_required(login_url='/login/')
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


@login_required(login_url='/login/')
@user_passes_test(check_user_settings, login_url='/manage/')
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
