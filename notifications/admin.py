from django.contrib import admin
from .models import Notification

# Register your models here.

class NotiificationAdmin(admin.ModelAdmin):
	list_display=['from_user', 'to_user', 'not_type']

admin.site.register(Notification, NotiificationAdmin)

