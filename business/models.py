from django.db import models
from django.contrib.auth.models import User
from urllib.parse import urlparse


class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	image = models.ImageField('Profile Image', upload_to='Image/Settings/ProfileImages', 
		max_length=500, default='dummy.png')
	language = models.CharField('Langauge', default='English', max_length=50)
	# user, image, language

	def __str__(self):
		return self.user.first_name

	def my_reviews(self):
		return Review.objects.filter(user=self.user.id)

	def my_reviews_count(self):
		return Review.objects.filter(user=self.user.id).count()


class Category(models.Model):
	name = models.CharField('Name', max_length=200)
	date_created = models.DateTimeField('Date Created', auto_now_add=True)
	# name,

	def __str__(self):
		return self.name

	def my_businesses(self):
		return Business.objects.filter(category= self.id)


class Business(models.Model):
	name = models.CharField('Business Name', max_length=50, unique=True)
	image = models.ImageField('Image', upload_to='Image/Business/Profile/', max_length=500, 
		default='dummy.png')
	category = models.ForeignKey(Category, on_delete=models.CASCADE)
	description = models.CharField('Description', max_length=1200, blank=True)
	website = models.CharField('Website', max_length=150, blank=True, null=True)
	email = models.CharField('Email', max_length=50, blank=True, null=True)
	phone_number = models.CharField('Phone Number', max_length=50, blank=True, null=True)
	country = models.CharField('Country', max_length=50)
	county = models.CharField('County', max_length=50)
	town = models.CharField('Town', max_length=50)
	status = models.CharField('Status', max_length=50, default="unverified")
	date_created = models.DateTimeField('Date Created', auto_now_add=True)

	def __str__(self):
		return self.name

	def website_name(self):
		website = self.website
		domain = urlparse(website).netloc
		return domain

	def my_reviews(self):
		return Review.objects.filter(business=self.id)

	def rating(self):
		reviews = Review.objects.filter(business=self.id)
		rating_sum = 0
		for review in reviews:
			rating_sum = rating_sum + review.rating
		if rating_sum > 0:
			rating = (rating_sum/reviews.count()) 
			return round(rating, 1)
		else:
			return 0

	def rating_remarks(self):
		reviews = Review.objects.filter(business=self.id)
		rating_sum = 0
		for review in reviews:
			rating_sum = rating_sum + review.rating
		if rating_sum > 0:
			rating = (rating_sum/reviews.count()) 
			rating = round(rating, 1)
			if rating > 4.4:
				return 'Excellent'
			elif rating > 3.4:
				return 'Great'
			elif rating > 2.4:
				return 'Average'
			elif rating > 1.4:
				return 'Poor'
			else:
				return 'Bad'
		else:
			return 'Not Rated'

	def reviews_count(self):
		return Review.objects.filter(business=self.id).count()

	def excellent_percentage(self):
		reviews = Review.objects.filter(business=self.id)
		if reviews.count() > 0 :
			excellent_reviews = reviews.filter(rating__gt=4.4)
			percentage = (excellent_reviews.count()/reviews.count())*100
			return round(percentage)
		else:
			return 0

	def great_percentage(self):
		reviews = Review.objects.filter(business=self.id)
		if reviews.count() > 0 :
			great_reviews = reviews.filter(rating__gt=3.4, rating__lte=4.4)
			percentage = (great_reviews.count()/reviews.count())*100
			return round(percentage)
		else:
			return 0

	def average_percentage(self):
		reviews = Review.objects.filter(business=self.id)
		if reviews.count() > 0 :
			average_reviews = reviews.filter(rating__gt=2.4, rating__lte=3.4)
			percentage = (average_reviews.count()/reviews.count())*100
			return round(percentage)
		else:
			return 0
	
	def poor_percentage(self):
		reviews = Review.objects.filter(business=self.id)
		if reviews.count() > 0 :
			poor_reviews = reviews.filter(rating__gt=1.4, rating__lte=2.4)
			percentage = (poor_reviews.count()/reviews.count())*100
			return round(percentage)
		else:
			return 0
		
	def bad_percentage(self):
		reviews = Review.objects.filter(business=self.id)
		if reviews.count() > 0 :
			bad_reviews = reviews.filter(rating__gt=0.0, rating__lte=1.4)
			percentage = (bad_reviews.count()/reviews.count())*100
			return round(percentage)
		else:
			return 0
		


		

class Review(models.Model):
	business = models.ForeignKey(Business, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	rating = models.IntegerField('Rating', default=0)
	title = models.CharField('Title', max_length=50, blank=True, null=True)
	review = models.CharField('Review', max_length=1200, blank=True, null=True)
	date_created = models.DateTimeField('Date Created', auto_now_add=True)
	# business, user, rating, title, review

	def __str__(self):
		return self.title 

	def user_profile(self):
		return UserProfile.objects.get(user=self.user.id)

	def user_reviews_count(self):
		return Review.objects.filter(user=self.user.id).count()


class Confirm_Email(models.Model):
	email = models.CharField('Email', max_length=50)
	code = models.IntegerField('Code')
	name = models.CharField('Name', max_length=20, null=True)
	date_created = models.DateTimeField('Date Created', auto_now_add=True)
	# email, code, name