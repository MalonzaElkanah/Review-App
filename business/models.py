from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg

from urllib.parse import urlparse


class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	image = models.ImageField('Profile Image', upload_to='Image/Settings/ProfileImages', 
		max_length=500, default='Image/Settings/ProfileImages/dummy.png')
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

	def my_businesses_ordered(self):
		businesses = Business.objects.filter(category= self.id)
		ordered_businesses = []
		for business in businesses:
			ordered_businesses = ordered_businesses + [business]
		for dummy in ordered_businesses:
			index = 0
			for business in ordered_businesses:
				if (index+1) == len(ordered_businesses):
					break
				else:
					if business.rating() < ordered_businesses[index+1].rating():
						ordered_businesses[index] = ordered_businesses[index+1]
						ordered_businesses[index+1] = business
				index += 1
		return ordered_businesses


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
	# name, image, category, description, website, email, phone_number, country, county, town, status

	def __str__(self):
		return self.name

	def website_name(self):
		website = self.website
		domain = urlparse(website).netloc
		return domain

	def my_reviews(self):
		return Review.objects.filter(business=self.id)

	def rating(self):
		rating = Review.objects.filter(business=self.id).aggregate(Avg('rating'))
		if rating['rating__avg'] is not None:
			return round(rating['rating__avg'], 1)
		else:
			return 0

	def rating_remarks(self):
		rating = Review.objects.filter(business=self.id).aggregate(Avg('rating'))
		if rating['rating__avg'] is not None:
			rating = round(rating['rating__avg'], 1)
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

	def category_rank(self):
		businesses = self.category.my_businesses_ordered()
		count = 1
		for business in businesses:
			if business.rating() == 0:
				return None
			else:
				if business.id == self.id:
					return count
			count = count + 1
		return None


		

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

	def remarks(self):
		rating = self.rating
		if rating == 5:
			return 'Excellent'
		elif rating == 4:
			return 'Great'
		elif rating == 3:
			return 'Average'
		elif rating == 2:
			return 'Poor'
		elif rating == 1:
			return 'Bad'
		else:
			return 'Bad'


class Confirm_Email(models.Model):
	email = models.CharField('Email', max_length=50)
	code = models.IntegerField('Code')
	name = models.CharField('Name', max_length=20, null=True)
	date_created = models.DateTimeField('Date Created', auto_now_add=True)
	# email, code, name