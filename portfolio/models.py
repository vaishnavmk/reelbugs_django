from django.db import models
from auth_app.models import User
import re
from django.utils.text import  slugify
from django.utils import timezone
from tinymce.models import HTMLField
from django.core.files.base import ContentFile
from PIL import Image, ImageOps
from PoetsDuel import settings
from io import BytesIO
import os
from django.shortcuts import reverse
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext

class Piece(models.Model):
	author=models.ForeignKey(User, related_name='pieces')
	title=models.CharField(max_length=50)
	public=models.BooleanField(default=False)
	slug=models.SlugField()
	created_on=models.DateTimeField()
	content=models.FileField(upload_to='pieces/content', null=True)
	thumb=models.ImageField(blank=True, null=True, upload_to='pieces/piece_thumbs')
	views=models.IntegerField(blank=True, default=0)
	plikes=models.ManyToManyField(User, related_name='pliked', blank=True)
	visibility=models.BooleanField(default=True)
	summary=models.CharField(max_length=800, default='A story on blumury')

	def get_absolute_url(self):
		return 'www.blumury.com'+reverse('read_piece', kwargs={'piece_slug': self.slug})

	def get_summary(self):
		with open(self.content.path) as f:
			c=f.read(1000)
		c=cleanhtml(c)
		dic={"&rsquo;":"'","&nbsp;":" ", "&ldquo;":"\"", "&rdquo;":"\""}
		for i,j in dic.items():
			c=c.replace(i,j)
		return c


	def like_count(self):
		return self.plikes.count()

	def publish(self, request):
		self.save()
		slug='%d %s'%(self.id, self.title)
		self.slug=slugify(slug)
		piece_file=ContentFile(request.session['piece_content'])
		del request.session['piece_content']
		self.content.save(str(self.id)+'.txt', piece_file, save=False)
		if not self.summary or len(self.summary)<100:
			self.summary=self.get_summary()
		self.save()

	def republish(self, request):
		self.save()
		slug='%d %s'%(self.id, self.title)
		self.slug=slugify(slug)
		self.content.delete()
		piece_file=ContentFile(request.session['piece_content'])
		del request.session['piece_content']
		self.content.save(str(self.id)+'.txt', piece_file, save=True)
		self.summary=self.get_summary()
		self.save()

	def gen_thumb(self, image):
		if self.thumb:
			os.remove(self.thumb.path)
		im=Image.open(image)
		im.convert('RGB')
		im=im.resize((71,85), Image.ANTIALIAS)
		a=BytesIO()
		im.save(a, format='jpeg', quality=95)
		av=a.getvalue()
		self.thumb.save(str(self.id)+'.pt.jpeg', ContentFile(av))


	def __str__(self):
		return 'Piece '+self.title

class Pcomment(models.Model):
	user=models.ForeignKey(User, on_delete=models.CASCADE)
	piece=models.ForeignKey(Piece, on_delete=models.CASCADE, related_name='comments')
	rant=models.CharField(max_length=500, blank=False)
	posted_on=models.DateTimeField(auto_now_add=True)
	upvotes=models.ManyToManyField(User, related_name='pups')

	class Meta():
		ordering=['-posted_on']
	
	def __str__(self):
		return 'Pcmt %d %s' %(self.id,self.piece)
