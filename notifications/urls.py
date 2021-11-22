from django.conf.urls import url
import notifications.views as views

urlpatterns=[
	url(r'last_notifs/$', views.last_notifs, name='last_notifs'),
	url(r'notifications/$', views.notifications, name='notifications'),
	url(r'check_notifs/$', views.check_notifs, name='check_notifs')
]
