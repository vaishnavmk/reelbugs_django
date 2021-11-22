from django.contrib.sitemaps import Sitemap
from writers_block.models import Movie, TV, Celeb
from django.shortcuts import reverse

class MovieSiteMap(Sitemap):
	changefreq='hourly',
	priority=0.8

	def items(self):
		return Movie.objects.all()

class TVSiteMap(Sitemap):
	changefreq='hourly',
	priority=0.8

	def items(self):
		return TV.objects.all()

class CelebSiteMap(Sitemap):
	changefreq='hourly',
	priority=0.8

	def items(self):
		return Celeb.objects.all()

class StaticSiteMap(Sitemap):
	priority=0.7
	changefreq='daily'

	def items(self):
		return ['index2', 'about']

	def location(self, item):
		return reverse(item)

		
		