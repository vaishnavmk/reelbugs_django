from django.contrib import admin
from .models import Profile, User

# Register your models here.

class ProfileAdmin(admin.ModelAdmin):
	list_display=['user', 'get_userid']

	def get_userid(self, obj):
		return obj.user.id


admin.site.register(Profile, ProfileAdmin)
