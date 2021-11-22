from django.db import models
from auth_app.models import User
from portfolio.models import Piece, Pcomment
from writers_block.models import Block, Comment
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Notification(models.Model):
	LIKE='L'
	COMMENT='C'
	FOLLOW='F'
	SHARE='S'
	P_LIKE='P'
	P_COMMENT='R'
	P_CREATED='B'

	NOTIFICATION_CHOICES=(
		(LIKE,'Liked'),
		(COMMENT, 'Commented'),
		(FOLLOW, 'Followed'),
		(SHARE,'Shared'),
		(P_LIKE,'Piece Liked'),
		(P_COMMENT, 'Piece Commented'),
		(P_CREATED, 'Piece Written')
	)

	_LIKE_TEXT = '<a href="/users/profile/{0}">{1}</a> liked your <a href="/index/block_view/{2}/">block</a>'
	_COMMENT_TEXT = '<a href="/users/profile/{0}">{1}</a> commented on your <a href="/index/block_view/{2}/">block</a>' 
	_FOLLOW_TEXT='<a href="/users/profile/{0}">{1}</a> followed you'
	_SHARE_TEXT='<a href="/users/profile/{0}">{1}</a> shared your <a href="/index/block_view/{2}/">block</a>'
	_P_LIKE_TEXT = '<a href="/users/profile/{0}">{1}</a> liked your <a href="/portfolio/read_piece/{2}/">piece</a>'
	_P_COMMENT_TEXT= '<a href="/users/profile/{0}">{1}</a> commented on your <a href="/portfolio/read_piece/{2}/">piece</a>'
	_P_CREATED_TEXT= '<a href="/users/profile/{0}">{1}</a> wrote a <a href="/portfolio/read_piece/{2}/">piece</a>'


	from_user=models.ForeignKey(User, related_name='sent_notifs')
	to_user=models.ForeignKey(User, related_name='notifs')
	at_time=models.DateTimeField(auto_now_add=True)
	not_type=models.CharField(max_length=1, choices=NOTIFICATION_CHOICES)
	block=models.ForeignKey(Block, null=True, blank=True)
	piece=models.ForeignKey(Piece, null=True, blank=True)
	read=models.BooleanField(default=False)

	class Meta():
		ordering=['-at_time']


	def __str__(self):
		if self.not_type==self.LIKE:
			return self._LIKE_TEXT.format(self.from_user.id, 
				self.from_user.username,
				self.block.id,
			)
		elif self.not_type==self.COMMENT:
			return self._COMMENT_TEXT.format(self.from_user.id,
				self.from_user.username,
				self.block.id
			)
		elif self.not_type==self.SHARE:
			return self.SHARE_TEXT.format(self.from_user.id,
				self.from_user.username,
				self.block.id
			)
		elif self.not_type==self.P_LIKE:
			return self._P_LIKE_TEXT.format(self.from_user.id,
				self.from_user.username,
				self.piece.slug
			)
		elif self.not_type==self.P_COMMENT:
			return self._P_COMMENT_TEXT.format(self.from_user.id,
				self.from_user.username,
				self.piece.slug
			)
		elif self.not_type==self.P_CREATED:
			return self._P_LIKE_TEXT.format(self.from_user.id,
				self.from_user.username,
				self.piece.slug
			)
		else:
			return self._FOLLOW_TEXT.format(self.from_user.id,
				self.from_user.username
			)
