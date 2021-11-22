from django.contrib import admin
from .models import Piece, Pcomment

# Register your models here.

class PieceAdmin(admin.ModelAdmin):
	list_display=['author', 'id', 'slug', 'created_on', 'views', 'visibility']

class PcomAdmin(admin.ModelAdmin):
	list_display=['piece', 'user', 'id', 'posted_on']

admin.site.register(Piece, PieceAdmin)
admin.site.register(Pcomment, PcomAdmin)