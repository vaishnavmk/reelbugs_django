from writers_block import views 
from django.conf.urls import url
from django.views.generic import TemplateView

urlpatterns=[
	url(r'^$', views.index2, name='index2'),

	#Anonymous block urls
	url(r'^amdw/(?P<movie_id>\d+)/$', views.anon_mblock, name='anon_movie_block'),
	url(r'^atdw/(?P<tv_id>\d+)/$', views.anon_tblock, name='anon_tv_block'),
	url(r'^acw/$', views.write_anon_comment, name='write_anon_comment'),
	url(r'^abd/$', views.delete_anon_block, name='delete_anon_block'),
	url(r'^acd/$', views.delete_anon_comment, name='delete_anon_comment'),
	url(r'^acu/$', views.upvote_anon_comment, name='upvote_anon_comment'),
	url(r'^abl/$', views.like_anon_block, name='like_anon_block'),
	url(r'^subscribe/$', views.subscribe, name='subscribe'),
    url(r'^block_view/(?P<block_id>\d+)/$', views.block_view, name='block_view'),
    url(r'^md/(?P<movie_id>\d+)/$', views.movie_detail, name='movie_detail'),
    url(r'^td/(?P<tv_id>\d+)/$', views.tv_detail, name='tv_detail'),
    url(r'^pd/(?P<person_id>\d+)/$', views.person_detail, name='person_detail'),
    url(r'^mvc/$', views.index2, name='index2'),
    url(r'^about/$', views.about, name='about'),
    url(r'^privacy_policy/$', TemplateView.as_view(template_name='writers_block/privacy_policy.html'), name='privacy_policy'),
    url(r'^contact/$', TemplateView.as_view(template_name='writers_block/contact.html'), name='contact'),
    url(r'^artwork/$', views.artwork, name='artwork'),
    url(r'^submit_fanart', views.submit_fanart, name='submit_fanart')


]