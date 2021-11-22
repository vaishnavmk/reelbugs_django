from django.shortcuts import render
from .models import Notification
from auth_app.models import User, Profile
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

# Create your views here.
def last_notifs(request):
	notifs=Notification.objects.filter(to_user=request.user, read=False)
	for notif in notifs:
		notif.read=True
		notif.save()
	return render(request, 'notifications/last_notifs.html', {'notifs':notifs})


@login_required
def notifications(request):
	Notification.objects.filter(to_user=request.user).filter(read=True).delete()
	notifications = Notification.objects.filter(to_user=request.user).exclude(from_user=request.user)
	return render(request, 'notifications/notifications.html',{'notifs': notifications})

@login_required
def check_notifs(request):
	notifications=Notification.objects.filter(to_user=request.user, read=False).exclude(from_user=request.user)
	return HttpResponse(len(notifications))



	
