from django import forms
from django.forms import ModelForm
from .models import UserProfile


class UserProfileForm(ModelForm):
	class Meta:
		model = UserProfile
		fields = ( 'user', 'image', 'language')
		widgets = {
			'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
		}