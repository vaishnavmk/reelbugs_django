from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils.six import StringIO
import os
from PoetsDuel import settings
from PIL import Image, ImageOps
from django.shortcuts import reverse



class Fanart(models.Model):
	piece=models.TextField(blank=True, null=True)
	approved=models.BooleanField(default=False)

	def __str__(self):
		return 'Fan '+self.piece

class Movie(models.Model):
	movie_id=models.IntegerField(blank=True, null=True, unique=True)
	fanart=models.ManyToManyField(Fanart, related_name='movie')

	def get_absolute_url(self):
		return reverse('movie_detail', kwargs={'movie_id': self.movie_id})

	def __str__(self):
		return 'Movie'+str(self.movie_id)

class TV(models.Model):
	tv_id=models.IntegerField(blank=True, null=True, unique=True)
	fanart=models.ManyToManyField(Fanart, related_name='tv')

	def get_absolute_url(self):
		return reverse('tv_detail', kwargs={'tv_id': self.tv_id})

	def __str__(self):
		return 'TV'+str(self.tv_id)


class Celeb(models.Model):
	celeb_id=models.IntegerField(blank=True, null=True, unique=True)

	def get_absolute_url(self):
		return reverse('person_detail', kwargs={'person_id': self.celeb_id})

	def __str__(self):
		return 'Celeb'+str(self.celeb_id)


# A block post with likes, the related series, and content with methods for like counting and detail url page.

class Block(models.Model):
	author=models.ForeignKey(User, on_delete=models.CASCADE, related_name='blocks', null=True, blank=True)
	auth_name=models.CharField(max_length=25,null=True, blank=True)
	content=models.CharField(max_length=4000, blank=False, null=False)
	posted_on=models.DateTimeField()
	image=models.ImageField(upload_to='block_images/' ,blank=True, null=True)
	likes=models.ManyToManyField(User, related_name='liked', blank=True)
	movie=models.ForeignKey(Movie, related_name='movie', blank=True, null=True)
	tv=models.ForeignKey(TV, related_name='tv', blank=True, null=True)


	def like_count(self):
		return self.likes.count()

	def save(self, *args, **kwargs):
		super(Block, self).save()
		if self.image:
			im=Image.open(settings.MEDIA_ROOT+'/'+self.image.name)
			basewidth=420
			per=basewidth/float(im.size[0])
			h=int(float(im.size[1])*float(per))
			im=im.resize((basewidth,h), Image.ANTIALIAS)
			im.save(settings.MEDIA_ROOT+'/'+self.image.name, quality=60)

	def get_absolute_url(self):
		return(reverse('block_view', kwargs={'block_id':self.id}))

	def post_it(self):
		self.posted_on=timezone.now()
		self.save()

	def delete_it(self):
		self.delete()

	def __str__(self):
		return '%s' % (self.content[:40]+'...')

class Anon_block(models.Model):
	auth_name=models.CharField(max_length=25,null=True, blank=True)
	content=models.CharField(max_length=4000, blank=False, null=False)
	posted_on=models.DateTimeField()
	ip=models.CharField(max_length=150, null=True, blank=True)
	profile=models.CharField(default='8fcc6c61d0b597cf5b8ade2722062a2e5', max_length=33)
	image=models.ImageField(upload_to='block_images/' ,blank=True, null=True)
	likes=models.IntegerField(default=0)
	movie=models.ForeignKey(Movie, related_name='rel_movie', blank=True, null=True)
	tv=models.ForeignKey(TV, related_name='rel_tv', blank=True, null=True)



	def save(self, *args, **kwargs):
		super(Anon_block, self).save()
		if self.image:
			im=Image.open(settings.MEDIA_ROOT+'/'+self.image.name)
			if im.format=='GIF':
				im.save(settings.MEDIA_ROOT+'/'+self.image.name, save_all=True,  quality=90)
			else:
				basewidth=420
				per=basewidth/float(im.size[0])
				h=int(float(im.size[1])*float(per))
				im=im.resize((basewidth,h), Image.ANTIALIAS)
				im.save(settings.MEDIA_ROOT+'/'+self.image.name, quality=90)

	def get_absolute_url(self):
		return(reverse('block_view', kwargs={'block_id':self.id}))

	def post_it(self):
		self.posted_on=timezone.now()
		self.save()

	def delete_it(self):
		self.delete()

	def __str__(self):
		return '%s' % (self.content[:40]+'...')


class Anon_comment(models.Model):
	profile=models.CharField(default='8fcc6c61d0b597cf5b8ade2722062a2e5', max_length=33)
	rant=models.CharField(max_length=500, blank=False)
	block=models.ForeignKey(Anon_block, on_delete=models.CASCADE, related_name='comments')
	posted_on=models.DateTimeField()
	upvotes=models.IntegerField(default=0)

	class Meta():
		ordering=['-posted_on']

	def post_it(self):
		self.posted_on=timezone.now()
		self.save()

	def __str__(self):
		return 'Cmnt %d %s' %(self.id,self.block)


#A comment which stores the comment, user, posted date and the related block.
class Comment(models.Model):
	user=models.ForeignKey(User, on_delete=models.CASCADE)
	block=models.ForeignKey(Block, on_delete=models.CASCADE, related_name='comments')
	rant=models.CharField(max_length=500, blank=False)
	posted_on=models.DateTimeField()
	upvotes=models.ManyToManyField(User, related_name='bups')

	class Meta():
		ordering=['-posted_on']

	def post_it(self):
		self.posted_on=timezone.now()
		self.save()

	def __str__(self):
		return 'Cmnt %d %s' %(self.id,self.block)






