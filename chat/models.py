from django.db import models
from auth_app.models import User
from django.utils import timezone

class Message_text(models.Model):
	from_user=models.ForeignKey(User, related_name='sent_chat')
	to_user=models.ForeignKey(User, related_name='recieved_chat')
	message=models.CharField(max_length=1000)
	read=models.BooleanField(default=False)
	posted_on=models.DateTimeField(default=timezone.now)

	def __str__(self):
		return ','.join([self.from_user.username,self.to_user.username])

