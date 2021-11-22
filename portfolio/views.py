from django.shortcuts import render, get_object_or_404, reverse
from django.contrib.auth.decorators import login_required
from .forms import WritePiece_Form, CreatePiece_Form, EditPiece_Form
from .models import Piece, Pcomment
from PoetsDuel import settings
from django.http import HttpResponse
import os
from django.shortcuts import redirect
from django.utils import timezone
from django.contrib import messages
from notifications.models import Notification
from django.forms.models import model_to_dict
from django.http import JsonResponse
from random import randint
from django.db.models import Q
from django.core.serializers import serialize

# Create your views here.

def pieces_list(request):
	pieces=Piece.objects.filter(visibility=True)
	return render(request, 'portfolio/pieces.html', {'pieces':pieces})

def read_piece(request, piece_slug):
	p=get_object_or_404(Piece, slug=piece_slug)
	p.views+=1
	p.save(update_fields=['views'])
	p.content.open(mode='rb')
	content=p.content.read()
	p.content.close()
	return render(request, 'portfolio/read_piece.html', {'content':content,'piece':p})


@login_required
def write_piece(request):
	if request.method=="POST":
		form=WritePiece_Form(request.POST)
		if form.is_valid():
			request.session['piece_content']=form.cleaned_data['content']
			request.session['piece_content']=request.session['piece_content'].replace('<img src="http://', '<img src="https://images.weserv.nl/?url=')
			return redirect('create_piece')
		else:
			return render(request, 'portfolio/write_piece1.html', {'form':form})
	else:
		form=WritePiece_Form()
		return render(request, 'portfolio/write_piece1.html', {'form':form})

@login_required
def edit_piece_content(request, piece_id):
	piece=get_object_or_404(Piece, pk=piece_id)
	if request.method=="POST":
		form=WritePiece_Form(request.POST)
		if form.is_valid():
			request.session['piece_content']=form.cleaned_data['content']
			return redirect(reverse('edit_piece', kwargs={'piece_id':piece.id}))
		else:
			return render(request, 'portfolio/edit_piece_content.html', {'form':form})
	else:
		piece.content.open(mode='rb')
		pcontent=piece.content.read()
		return render(request, 'portfolio/edit_piece_content.html', {'form':WritePiece_Form(), 'pcontent':pcontent})


@login_required
def edit_piece(request, piece_id):
	piece=get_object_or_404(Piece, pk=piece_id)
	if request.method=='POST':
		form=EditPiece_Form(request.POST, request.FILES)
		if form.is_valid():
			pObj=form.cleaned_data
			piece.title=pObj['title']
			if pObj['thumb']:
				piece.gen_thumb(pObj['thumb'])
			piece.republish(request)
			return redirect('piece_manager')
		else:
			return render(request, 'portfolio/edit_piece.html', {'form':form, 'piece':piece})
	else:
		return render(request, 'portfolio/edit_piece.html', {'form':EditPiece_Form(), 'piece':piece})



@login_required
def create_piece(request):
	if request.method=='POST':
		form=CreatePiece_Form(request.POST, request.FILES)
		if form.is_valid():
			f=form.cleaned_data
			p=Piece(author=request.user,
					title=f['title'],
					created_on=timezone.now(),
					summary=f['summary']
					)
			p.gen_thumb(f['thumb'])
			p.publish(request)
			return redirect('piece_manager')
		else:
			return render(request, 'portfolio/create_piece.html', {'form':form})
	else:
		return render(request, 'portfolio/create_piece.html', {'form':CreatePiece_Form()})

def delete_piece(request):
	if request.method=='POST':
		piece_id=request.POST.get('piece_id', None)
		piece=get_object_or_404(Piece, pk=int(piece_id))
		piece.delete()
		return JsonResponse({'done':True})

def like_piece(request):
	if request.method=='POST':
		piece_id=request.POST.get('piece_id', None)
		piece=get_object_or_404(Piece, pk=int(piece_id))
		if request.user in piece.plikes:
			piece.plikes.remove(request.user)
		else:
			piece.plikes.add(request.user)
		return HttpResponse()
	

@login_required
def write_pcomment(request):
	if request.method=='POST':
		piece_id=request.POST.get('piece_id', None)
		piece=get_object_or_404(Piece, pk=int(piece_id))
		new_comment=Pcomment(
			rant=request.POST.get('text'), 
			piece=piece,
			user=request.user)
		new_comment.save()
		Notification.objects.create(
			from_user=request.user,
			to_user=piece.author,
			not_type='R',
			piece=piece)
		comment={'rant':new_comment.rant, 
		'user': new_comment.user.id, 
		'image_url': request.user.person.thumbnail.url, 
		'count': piece.comments.count(),
		'id':new_comment.id
		}			
		data={'comment': comment}
		return JsonResponse(data)

@login_required
def delete_pcomment(request):
	if request.method=='POST':
		c=get_object_or_404(Pcomment, pk=int(request.POST.get('pcid')))
		c.delete()
		return HttpResponse('')

@login_required
def up_pcom(request):
	if request.method=='POST':
		c=get_object_or_404(Pcomment, pk=int(request.POST.get('pcid')))
		if request.user in c.upvotes.all():
			c.upvotes.remove(request.user)
		else:
			c.upvotes.add(request.user)
	return HttpResponse('')


@login_required
def plike_piece(request):
	piece_id=request.POST.get('piece_id')
	p=get_object_or_404(Piece, pk=int(piece_id))
	if request.user in p.plikes.all():
		p.plikes.remove(request.user)
	else:
		p.plikes.add(request.user)
	return HttpResponse('')

@login_required
def piece_manager(request):
	pieces=request.user.pieces.all().order_by('-created_on')
	return render(request, 'portfolio/piece_manager.html', {'pieces':pieces})

@login_required
def change_visib(request):
	piece_id=request.POST.get('piece_id', None)
	piece=get_object_or_404(Piece, pk=piece_id)
	if piece.visibility:
		piece.visibility=False
		piece.save(update_fields=['visibility'])
		data={'visib': False}
	else:
		piece.visibility=True
		piece.save(update_fields=['visibility'])
		data={'visib':True}
	return JsonResponse(data)

def lucky_read(request):
	p=Piece.objects.filter(visibility=True)
	np=p.count()-1

	ran=randint(0,np)
	while True:
		if p[ran]:
			slug=p[ran].slug
			break
		else:
			ran=randint(0,np)

	return redirect(reverse('read_piece', kwargs={'piece_slug':slug}))

def piece_search(request):
	query=request.GET.get('query')
	p=Piece.objects.filter(Q(title__icontains=query)|Q(content__icontains=query), visibility=True)
	pieces=serialize('json', p)
	return HttpResponse(pieces)



