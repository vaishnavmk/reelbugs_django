
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from PoetsDuel import settings
import os
from PIL import ImageOps, Image
from io import BytesIO
from django.core.files.base import ContentFile
from io import StringIO, BytesIO
from hashlib import md5
from urllib.request import urlopen

#User Profile with followers, bio, avatar and thumbnail

class Profile(models.Model):
	
	user=models.OneToOneField(User, related_name='person')	
	me=models.TextField(null=True,blank=True, max_length=250)
	following=models.ManyToManyField('self', related_name='followers', symmetrical=False, blank=True)
	avatar=models.ImageField(upload_to='avatars/', default='/std_avatar.jpeg')
	thumbnail=models.ImageField(upload_to='thumbnails/', default='/std_thumb.jpeg')

	def get_thumb(self):
		if self.thumbnail:
			return self.thumbnail.url

	def get_av(self):
		if self.avatar:
			return self.avatar.url

	def gen_thumb(self, url):
		f=BytesIO(urlopen(url).read())
		im=Image.open(f)
		im.convert('RGB')
		new_thumb=ImageOps.fit(im, (50,50), Image.ANTIALIAS)
		t=BytesIO()
		new_thumb.save(t, format='jpeg', quality=90)
		th=t.getvalue()
		t.close()
		f.close()
		self.thumbnail.save(str(self.user.id)+'.jpeg', ContentFile(th), save=True)



	def gen_avatar_n_thumb(self, image):
		im=Image.open(image)
		f=im.format.lower()
		im.convert('RGB')
		new_avatar=ImageOps.grayscale(im)
		new_avatar=ImageOps.fit(new_avatar, (200,200), Image.ANTIALIAS)
		new_thumb=ImageOps.fit(im, (50,50), Image.ANTIALIAS)
		#saved to bytes coz of rgb conversion (flag)
		a=BytesIO()
		t=BytesIO()
		if f=='gif':
			new_avatar.save(a, save_all=True, format=f, quality=70)
			new_thumb.save(t, save_all=True, format=f, quality=90)
		else:
			new_avatar.save(a, format=f, quality=70)
			new_thumb.save(t, format=f, quality=90)
		av=a.getvalue()
		th=t.getvalue()
		a.close()
		t.close()
		#save new avatar and thumb (old ones deleted at the top of this method)
		self.avatar.save(str(self.user.id)+'.'+f, ContentFile(av))
		self.thumbnail.save(str(self.user.id)+'.'+f, ContentFile(th), save=True)



	def follower_count(self):
		return self.followers.all().count()


	def __str__(self):
		return str(self.user.username)


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

def save_user_profile(sender, instance, **kwargs):
    instance.person.save()


post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)


