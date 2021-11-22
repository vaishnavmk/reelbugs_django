from django.contrib import admin
from .models import Anon_block, Anon_comment, Fanart

# Register your models here.
class Anon_blockAdmin(admin.ModelAdmin):
	list_display=['auth_name', 'posted_on', 'movie', 'tv', 'ip']
	list_filter=('auth_name','movie_id', 'tv','ip')
	ordering=['-posted_on']

class FanartAdmin(admin.ModelAdmin):
	list_display=['approved', 'piece']


admin.site.register(Anon_block, Anon_blockAdmin)
admin.site.register(Anon_comment)
admin.site.register(Fanart, FanartAdmin)
