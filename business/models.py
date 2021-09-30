from django.db import models
from django.contrib.auth.models import User
from urllib.parse import urlparse


class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	image = models.ImageField('Profile Image', upload_to='Image/Settings/ProfileImages', 
		max_length=500, default='dummy.png')
	language = models.CharField('Langauge', default='English', max_length=50)


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



class Review(models.Model):
	business = models.ForeignKey(Business, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	rating = models.IntegerField('Rating', default=0)
	title = models.CharField('Title', max_length=50)
	review = models.CharField('Review', max_length=1200, blank=True, null=True)
	date_created = models.DateTimeField('Date Created', auto_now_add=True)

	def __str__(self):
		return self.title 


class Confirm_Email(models.Model):
	email = models.CharField('Email', max_length=50)
	code = models.IntegerField('Code')
	name = models.CharField('Name', max_length=20, null=True)
	date_created = models.DateTimeField('Date Created', auto_now_add=True)
	# email, code, name