from django.conf.urls import url, include
from auth_app import views
from django.contrib.auth.views import login, logout_then_login, password_reset, password_reset_done, password_reset_confirm, password_reset_complete


urlpatterns=[
#    url(r'^signup/$', views.signup, name='signup'),
	url(r'^signin/$', login, name='signin'),
#	url(r'^username_taken/$', views.username_taken, name='username_taken'),
#	url(r'^password_reset/$', password_reset, name='password_reset'),
#	url(r'^password_reset/done/$', password_reset_done, name='password_reset_done'),
#	url(r'^password_reset/confirm/(?P<uidb64>[-\w+]+)/(?P<token>[-\w+]+)/$', password_reset_confirm, name='password_reset_confirm'),
#	url(r'^password_reset/complete/$', password_reset_complete, name='password_reset_complete'),
	url(r'^signout', logout_then_login, name='signout'),
    url(r'^profile/(?P<pk>\d+)/$', views.ProfileView.as_view(), name='profile_view'),
    url(r'^profile_edit/$', views.profile_edit, name='profile_edit'),
    url(r'^fu/(?P<foll_id>\d+)/$', views.follow_user, name='follow_user'),
    url(r'^fubw/(?P<foll_id>\d+)/$', views.foll_user_bw, name='foll_user_bw'),
    url(r'^check_creds/$', views.check_creds, name='check_creds'),
    url(r'^hover_profile/(?P<userid>\d+)/$', views.hover_profile, name='hover_profile')
]
