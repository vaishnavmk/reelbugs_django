from django.contrib.auth import logout, login, authenticate
from .models import Profile, User
from .forms import Register, ProfileEditForm
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib import messages
from django.views.generic import DetailView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from writers_block.forms import Comment_form
from PoetsDuel import settings
from PIL import Image, ImageOps
from django.http import JsonResponse, HttpResponse
from io import BytesIO
from hashlib import md5
from urllib.request import urlopen
from django.core.files.base import ContentFile


def signin(request):
	if request.user.is_authenticated():
		return redirect('index2')
	else:
		return redirect('signin')

def signup(request):
	if request.user.is_authenticated():
		return redirect('index2')
	if request.method=='POST':
		form=Register(request.POST)
		if form.is_valid():
			username=form.cleaned_data['username']
			email=form.cleaned_data['email']
			password=form.cleaned_data['password']
			User.objects.create_user(username=username, email=email, password=password)
			user=authenticate(username=username, password=password)
			login(request, user)
			return redirect('index2')
		else:
			return render(request, 'auth_app/signup1.html', {'form':form})
	else:
		return render(request, 'auth_app/signup1.html', {'form':Register()})

#DeatilView for User Profiles by pk on url
class ProfileView(LoginRequiredMixin, DetailView):
	model=User
	context_object_name='user'
	template_name="auth_app/profile.html"

	def get_context_data(self, **kwargs):
		context=super(ProfileView, self).get_context_data(**kwargs)
		context['comment_form']=Comment_form()
		context['block_list']=self.object.blocks.all().order_by('-posted_on')
		context['settings']=settings
		context['recent_pieces']=self.object.pieces.order_by('-created_on')[:10]
		return context


def hover_profile(request, userid):
	user=get_object_or_404(User, pk=userid)
	data={'me':user.person.me, 'dp':user.person.thumbnail.url, 'followers': user.person.follower_count(), 'name':user.username}
	return JsonResponse(data)

@login_required
def profile_edit(request):
	if request.method=='POST':
		form=ProfileEditForm(request.POST, request.FILES)
		
		if form.is_valid():
			p=request.user.person
			proObj=form.cleaned_data
			if proObj['me']:
				p.me=proObj['me']
			# generate avatar and thumb or else save	
			if proObj['avatar']:
				p.gen_avatar_n_thumb(proObj['avatar'])
			else:
				p.save()
			return redirect('profile_view', pk=request.user.id)
		else:
			return render(request, 'auth_app/profile_edit.html', {'form':form,})

	else:
		form=ProfileEditForm()
		return render(request, 'auth_app/profile_edit.html', {'form':form,})


@login_required
def follow_user(request, foll_id):
	foll=Profile.objects.get(pk=foll_id)
	if foll not in request.user.person.following.all():
		request.user.person.following.add(foll)
		return JsonResponse({'foll':True})
	else:
		request.user.person.following.remove(foll)
		return JsonResponse({'foll':False})

@login_required
def foll_user_bw(request, foll_id):
	foll=Profile.objects.get(pk=foll_id)
	if foll not in request.user.person.following.all():
		request.user.person.following.add(foll)
	else:
		request.user.person.following.remove(foll)
	return redirect(reverse('profile_view', kwargs={'pk':foll_id}))
	


def username_taken(request):
	username=request.GET.get('username', None)
	data={
	'taken':User.objects.filter(username__iexact=username).exists()
	}
	return JsonResponse(data)

def check_creds(request):
	username=request.GET.get('username', None)
	password=request.GET.get('password', None)
	user=authenticate(username=username, password=password)
	if user:
		data={'creds':1}
	else:
		data={'creds':0}
	return JsonResponse(data)


			