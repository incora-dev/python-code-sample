from django import forms
from .models import User, UserProfile
from django.shortcuts import get_object_or_404

class UserCreateForm(forms.Form):
	email = forms.CharField(required= True)
	password = forms.CharField(required= True)

class UserUpdateForm(forms.Form):
	email = forms.CharField(required= False)
	password = forms.CharField(required= False)

class UserCreateProfileForm(forms.Form):
	name = forms.CharField(required= False)
	photo_name = forms.CharField(required= False)
	photo_url = forms.CharField(required= False)

class UserUpdateProfileForm(forms.Form):
	name = forms.CharField(required= False)
	photo_name = forms.CharField(required= False)
	photo_url = forms.CharField(required= False)


class UserFormCreator:

	def __init__(self, user_data):
		user_form_data = {}
		profile_form_data = {}
		self.top_error = {}

		if 'id' in user_data:
			self.user_form = UserCreateForm
			self.profile_form = UserCreateProfileForm

			self.user = get_object_or_404(User, pk= user_data['id'])
			self.profile = get_object_or_404(UserProfile, user= user)

		else:
			self.user_form = UserUpdateForm
			self.profile_form = UserUpdateProfileForm

			self.user = User()
			self.profile = UserProfile()

		for field, _ in self.user_form.base_fields.items():
			user_form_data[field] = user_data[field]

		for field, _ in self.profile_form.base_fields.items():
			profile_form_data[field] = user_data[field]

		self.user_form = self.user_form(user_form_data)
		self.profile_form = self.profile_form(profile_form_data)

	def validate(self, form):
		if not form.is_valid():
			field_name, errors = form.errors.items()[0]
			self.top_error[field_name] = errors[0]
			return False
		return True

	def is_valid(self):
		return self.validate(self.user_form) and self.validate(self.profile_form) and True

	def save(self):
		self.user.update(**self.user_form.cleaned_data)
		self.profile.update(**self.profile_form.cleaned_data)
		self.user.save()
		self.profile.save()
		return self.user, self.profile




