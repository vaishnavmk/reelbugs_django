"""PoetsDuel URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
	https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
	1. Add an import:  from my_app import views
	2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
	1. Add an import:  from other_app.views import Home
	2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
	1. Import the include() function: from django.conf.urls import url, include
	2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include 
from django.contrib import admin
from django.contrib.sitemaps import views
from PoetsDuel import settings
from django.conf.urls.static import static
from writers_block.sitemaps import MovieSiteMap, TVSiteMap, CelebSiteMap, StaticSiteMap
import writers_block

sitemaps={
	'movies':MovieSiteMap(), 'tv':TVSiteMap(), 'celeb':CelebSiteMap(), 'static':StaticSiteMap()
}

urlpatterns = [
#    url(r'^social-auth/', include('social_django.urls', namespace='social')),
	url(r'^index/', include('writers_block.urls')),
	url(r'^$', writers_block.views.index2, name='landing'),
	url(r'^uruliyililorumuralifszdfsff/', include(admin.site.urls)),
	url(r'^users/', include('auth_app.urls')),
	url(r'^sitemap\.xml$', views.index, {'sitemaps': sitemaps}),
	url(r'^sitemap-(?P<section>.+)\.xml$', views.sitemap, {'sitemaps': sitemaps},name='django.contrib.sitemaps.views.sitemap'),
	url(r'^BingSiteAuth\.xml', writers_block.views.bingxml, name='BingAuth'),
#    url(r'^tinymce/', include('tinymce.urls')),
#    url(r'^portfolio/', include('portfolio.urls')),
	url(r'^notifications/', include('notifications.urls')),
#    url(r'^chat/', include('chat.urls'))
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)



