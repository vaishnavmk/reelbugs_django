from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from PIL import Image, ImageOps
from .models import Profile


def Blacklisted(value):
	blacklist=['admin', 'settings', 'news', 'about', 'help', 'signin', 'signup', 'signout', 'terms', 'privacy', 'cookie', 'new', 'login', 'logout', 'administrator', 'join', 'account', 'username', 'root', 'blog', 'user', 'users', 'billing', 'subscribe','reviews', 'review', 'blog', 'blogs', 'edit', 'mail', 'email', 'home', 'job', 'jobs', 'contribute', 'newsletter', 'shop', 'profile', 'register', 'auth', 'authentication','campaign', 'config', 'delete', 'remove', 'forum', 'forums', 'download', 'downloads', 'contact', 'blogs', 'feed', 'faq', 'intranet', 'log', 'registration', 'search', 'explore', 'rss', 'support', 'status', 'static', 'media', 'setting', 'css', 'js','follow', 'activity', 'library']
	if value.lower() in blacklist:
		raise ValidationError("That's a reserved username")


def InvalidUsernameValidator(value):
	if '@' in value or '+' in value or '-' in value:
		raise ValidationError("That's not a valid username.")

def UniqueEmailValidator(value):
	if User.objects.filter(email__iexact=value).exists():
		raise ValidationError('User with this Email already exists.')

def UniqueUsernameIgnoreCaseValidator(value):
	if User.objects.filter(username__iexact=value).exists():
		raise ValidationError('User already exists.')

def lengthValidator(value):
	if len(value)>15:
		raise ValidationError("Username's too long")


class Register(forms.ModelForm):
	username=forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Username',}),required=True)
	email=forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Email'}), required=True)
	password=forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Password'}), required=True)

	class Meta:
		model=User
		fields=['username','email', 'password']

	def __init__(self, *args, **kwargs):
		super(Register, self).__init__(*args, **kwargs)
		self.fields['username'].validators.append(Blacklisted)
		self.fields['username'].validators.append(InvalidUsernameValidator)
		self.fields['username'].validators.append(UniqueUsernameIgnoreCaseValidator)
		self.fields['username'].validators.append(lengthValidator)
		self.fields['email'].validators.append(UniqueEmailValidator)





class ProfileEditForm(forms.Form):
	me=forms.CharField(widget=forms.Textarea(), max_length=150, required=False)
	avatar=forms.ImageField(required=False, error_messages={'invalid_image':'Our old battered server can only take jpegs and pngs',
															'invalid':'Our old battered server can only take jpegs and pngs'})
	
	
	def clean_image(self):
		avatar = self.cleaned_data["image"]
		# This won't raise an exception since it was validated by ImageField.
		im = Image.open(image)

		if im.format.lower() not in settings.ALLOWED_UPLOAD_IMAGES:
			raise forms.ValidationError(_("Unsupported file format. Supported formats are %s."
										  % ", ".join(settings.ALLOWED_UPLOAD_IMAGES)))

		image.seek(0)
		return image

	def __init__(self, *args, **kwargs):
		super(ProfileEditForm, self).__init__(*args, **kwargs)
		self.fields['avatar'].validators.append(avatar_size)

def avatar_size(value):
	if value.size> 3000000:
		raise forms.ValidationError('The image is too big for our battered server. Try to keep it under 3 mb')

#def cover_size(value):







