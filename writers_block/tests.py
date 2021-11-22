from django.test import TestCase
from django.utils import timezone
from writers_block.models import Block
from series.models import Series
from django.contrib.auth.models import User
from django.contrib.auth import login
import datetime
from django.urls import reverse

# Create your tests here

def create_block(content, author, days):
	time=timezone.now()+datetime.timedelta(days=days)
	return Block.objects.create(author=author, content=content, posted_on=time)

def createuser(username, password, email):
	u=User.objects.create_user(username=username,password=password, email=email)
	return u


def create_series(name):
	s=Series(name=name)
	s.save()
	return s

class IndexTestCases(TestCase):
	def test_index_no_login(self):
		a=createuser(username='dude', password='dude', email='dude@man.com')
		response=self.client.get(reverse('index'))
		self.assertEqual(response.status_code, 302)

	def test_index_set_empty(self):
		a=createuser(username='dude', password='dude', email='dude@man.com')
		self.client.login(username='dude', password='dude')
		response=self.client.get(reverse('index'))
		self.assertEqual(response.status_code, 200)
		self.assertQuerysetEqual(response.context['block_list'],[])

	def test_index_set_filled(self):
		a=createuser(username='dude', password='dude', email='dude@man.com')
		s=create_series(name='DD')
		u=createuser(username='man', password='man', email='dude@dude.com')
		s.subbed_users.add(u)
		self.client.login(username='man', password='man')
		b=create_block(content='do do do do', author=a, days=-2)
		c=create_block(content='me me me', author=a, days=-2)
		d=create_block(content='la la la', author=a, days=1)
		b.series.add(s)
		c.series.add(s)
		response=self.client.get(reverse('index'))
		self.assertQuerysetEqual(response.context['block_list'],['<Block: Block me>','<Block: Block do>'])



