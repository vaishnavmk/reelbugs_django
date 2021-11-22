from django.conf.urls import url
import portfolio.views as views

urlpatterns= [
	url(r'^write_piece/$', views.write_piece, name='write_piece'),
	url(r'^read_piece/(?P<piece_slug>[-\w]+)/$', views.read_piece, name='read_piece'),
	url(r'^create_piece/$', views.create_piece, name='create_piece'),
	url(r'^write_pcomment/$', views.write_pcomment, name='write_pcomment'),
	url(r'^piece_manager/$', views.piece_manager, name='piece_manager'),
	url(r'^change_visib/$', views.change_visib, name='change_visib'),
	url(r'^edit_piece/(?P<piece_id>\d+)/$', views.edit_piece, name='edit_piece'),
	url(r'^edit_piece_content/(?P<piece_id>\d+)/$', views.edit_piece_content, name='edit_piece_content'),
	url(r'^delete_piece/$', views.delete_piece, name='delete_piece'),
	url(r'^lucky_read/$', views.lucky_read, name='lucky_read'),
	url(r'^pieces_list/$', views.pieces_list, name='pieces_list'),
	url(r'^piece_search/$', views.piece_search, name='piece_search'),
	url(r'^plike_piece/$', views.plike_piece, name='plike_piece'),
	url(r'^up_pcom/$', views.up_pcom, name='up_pcom'),
	url(r'^delete_pcomment/$', views.delete_pcomment, name='delete_pcomment')
]