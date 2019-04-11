from django import forms
from django.contrib.auth.models import User
from internal.models import Profile

class ProfileForm(forms.ModelForm):
	username = forms.CharField()
	email = forms.EmailField()
	first_name = forms.CharField()
	last_name = forms.CharField()

	class Meta:
		model = User
		fields= ('username', 'email', 'first_name', 'last_name')

	def clean_email(self):
		username = self.cleaned_data.get('username')
		email = self.cleaned_data.get('email')
		if email and User.objects.filter(email=email).exclude(username=username).count():
			raise forms.ValidationError('This email is already in use! Please use a different email.')
		return email

	def save(self, commit=True):
		user = self.instance

		user.email = self.cleaned_data['email']
		user.username = self.cleaned_data['username']
		user.first_name = self.cleaned_data['first_name']
		user.last_name = self.cleaned_data['last_name']

		if commit:
			user.save()

		return user