from django.shortcuts import render, redirect
from .models import Message_text
from django.shortcuts import get_object_or_404
from auth_app.models import User
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q

@login_required
def send_message(request):
	if request.user.is_authenticated:
		if request.method=='POST':
			text, userid=request.POST.get('text'), request.POST.get('to')
			user=get_object_or_404(User, pk=int(userid))
			chat=Message_text.objects.create(from_user=request.user, to_user=user, message=text)
		return HttpResponse()
	return redirect('signin')


@login_required
def inbox(request):
	chats=Message_text.objects.filter(to_user=request.user).order_by('-posted_on')
	return render(request, 'chat/inbox.html', {'chats':chats})

@login_required
def message_view(request, id):
	chat=get_object_or_404(Message_text, pk=id)
	chat.read=True
	chat.save()
	chats=Message_text.objects.filter(Q(from_user=chat.from_user, to_user=chat.to_user)|Q(from_user=chat.to_user, to_user=chat.from_user)).order_by('-posted_on')
	return render(request ,'chat/message_view.html', {'chats':chats, 'other_user':chat.from_user})

@login_required
def check_inbox(request):
	yup=Message_text.objects.filter(to_user=request.user, read=False).exists()
	return JsonResponse({'yup': yup})


