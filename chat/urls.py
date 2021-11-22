from django.conf.urls import url
import chat.views as views


urlpatterns=[
	url(r'^send_message/$', views.send_message, name='send_message'),
	url(r'^inbox/$', views.inbox, name='inbox'),
	url(r'^message_view/(?P<id>[\d]+)/$', views.message_view, name='message_view'),
	url(r'^check_inbox', views.check_inbox, name='check_inbox')
]