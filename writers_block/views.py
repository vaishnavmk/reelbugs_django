from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.views import generic
from writers_block.models import Anon_block, Anon_comment, Movie, TV, Celeb, Fanart
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from .forms import Block_form, Comment_form, Mblock_form, Fanart_form
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView
from .models import User
from io import StringIO
from PoetsDuel import settings
from django.http import JsonResponse, HttpResponse
from django.core.serializers import serialize
from django.forms.models import model_to_dict
import json, datetime
from notifications.models import Notification
from portfolio.models import Piece
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import requests, json
from writers_block.static.ISO639_1 import ISO639_1 as langs
from ipware.ip import get_ip
from hashlib import md5
from random import randint
from PoetsDuel.settings import STATIC_ROOT, STATIC_URL
from django.core.mail import send_mail
from django.template.loader import render_to_string



random_auths=['Dricendiness', 'Orcemetrisected', 'Traitramentoist', 'Veracitandiness', 'Veracitivate', 'Cabalisticiting', 'Cabiliaticastigial', 'Cabalizincifyingly', 'Unacclaimablutions', 'Cabalinitratiatory', 'Orchardhanderstuffeurodollationeedlebaggining', 'Verbifurcatives', 'Mulatologotyled', 'Orcharangelicatabouts', 'Mullightning', 'Glacionabiliate', 'Orcharanglic', 'Dricentimetermiest', 'Shortwaverought', 'Shortwaveringes', 'Bombshellulates', 'Dricentipartmen', 'Glaciologarizes', 'Traitonitude', 'Shoshortwaverageeners', 'Gunslitheist', 'Cabiliatious', 'Glaciositivided', 'Traitorients', 'Assumatizaticizing', 'Cabalienians', 'Cabiliatomas', 'Shoshoshoest', 'Veracitieths', 'Dricentagons', 'Zoopatrolwomaniziness', 'Dricensurveillackener', 'Zoopatriotic', 'Assumptiones', 'Traliabillinist', 'Orcemergeoisellate', 'Unaccentertened', 'Mulatoriever', 'Bonatiatorience', 'Mulligencystemaker', 'Assuralistleggestibilist', 'Cabalisticathology', 'Orchardisoridation', 'Dricentiplexicompeded', 'Assumphanted', 'Zoopatroller', 'Orchardheads', 'Cabalistimabilibriquenes', 'Unaccepterandomnes', 'Bonaticasseeing', 'Cabalinitrockindlight', 'Gunslippetizers', 'Assumatology', 'Unacceptationablenter', 'Cabalitients', 'Verballooner', 'Orcharbinger', 'Dricenobiograms', 'Mulgatecrashies', 'Cabalienamounts', 'Assumationizationized', 'Unaccenteuse', 'Dricendanian', 'Orcemergeoisellees', 'Unaccommodation', 'Mulligatisfactoratefutabletive', 'Gunslippetizans', 'Bombshellulationes', 'Gunslippersnappraisal', 'Orchardballs', 'Mulatospheroffingling', 'Shoshoprivilegerenthumbscrevasculinization', 'Mulatosphore', 'Unacceptability', 'Unaccepteransomene', 'Cabalivating', 'Cabalinative', 'Orcharbountimes', 'Shoshoprizincifies', 'Hortwaverindulatitis', 'Gunslippersnappeasers', 'Glaciologicable', 'Shoshorsensitivist', 'Glacionaboutrigendotherabiliticialisecordepenciless', 'Verablutifielderintelepositude', 'Dricendinier', 'Gunslitheate', 'Assuralishly', 'Mulligatuatiablatient', 'Bombshellulositive', 'Mulatosphemeter', 'Orcemendationed', 'Shortwaveroughfarettonouncilloper', 'Mulligatotypicated', 'Mulgatoristical', 'Veracitanker', 'Cabalinizablutinizatization', 'Zoopatienter', 'Shortwaveroughened', 'Gunslippersnappliator', 'Mulligencumbilitieing', 'Gunslippersnapplaurelabeyantly', 'Mulgatorials', 'Shoshopriedicts', 'Trajectivalemen', 'Dricentimekeepenulatines', 'Dricentrionisherifiables', 'Unacclaimabluticiatingly', 'Mulatosphincalculatiousness', 'Orchardiscipiencients', 'Cabalinitroglyphic', 'Unaccentervationingly', 'Orcemetrichiselenings', 'Gunslippersnappetencillowed', 'Bonatibillboothesians', 'Zoopatrilitious', 'Unacceptabilitises', 'Mulligencies', 'Mulligatosis', 'Verbifurcations', 'Cabalignetic', 'Shortwaverinettled', 'Mulgatekeepiloganberrablene', 'Unabullfight', 'Glaciologrolled', 'Glacionaboutflates', 'Dricenobiogrificensurnamics', 'Zoopatrolled', 'Bonaticiamen', 'Zoopatriolettinous', 'Dricentimonists', 'Orcemetridgehammer', 'Glacionabilicussionlessness', 'Verbifurcatists', 'Unacclimactives', 'Unacceptarmigangstres', 'Unacclimacasehanderstriptionistic', 'Unaccommodatoriate', 'Orchardhandents', 'Assuralisher', 'Verballetristic', 'Bombshellularly', 'Assumptivitalic', 'Zoopatrilegiant', 'Orchardcover', 'Assumphinatizes', 'Assumphinist', 'Traitrarishings', 'Assumanizaticializers', 'Zoopatrimpreadjourage', 'Dricentrademonians', 'Unaccessions', 'Traitoneuras', 'Zoopatrolithologuessertistingiest', 'Orcharboutonwoollists', 'Zoopatrolitheticising', 'Orcharbougainsationingly', 'Unaccentermeasures', 'Bonatiate', 'Shoshovellinespike', 'Bombshellulositome', 'Glaciositive', 'Verbifurcatione', 'Unacclimaxes', 'Orchardbacks', 'Zoopatriminaria', 'Assuagemetrionishiftings', 'Bonaticasian', 'Unacclimaginian', 'Glaciationablensionature', 'Trajecturgiditimizzennes', 'Shoshoddiest', 'Unaccommodative', 'Zoopatriotously', 'Shortwaveroughness', 'Bonaticiated', 'Unacclimalizabited', 'Cabalinature', 'Shoshower', 'Dressioniall', 'Assuratellector', 'Gunslitheast', 'Zoopatienicationingly', 'Unacclaimablism', 'Dricented', 'Orcemergeablatilizablutiest', 'Trajectinous', 'Cabalistillbindelists', 'Verballyhock', 'Unacclimalizatient', 'Assuratelecastingling', 'Orchardbaggerer', 'Cabalistigmatizatitis', 'Dricendandelabrasiest', 'Dressimillstorm', 'Gunslitheliance', 'Cabilians', 'Unacclaimablish', 'Shoshorsemen', 'Bonatibility', 'Mulligatogenociatiate', 'Assuagemetricklies', 'Cabalitarnishments', 'Cabalitarily', 'Trajectinuousneakines', 'Orcharassablene', 'Mullightweights', 'Mullightedgeons', 'Gunslipperingemmology', 'Verablutinal', 'Dricensurcharlands', 'Orchardhanderstepsheatherpretationishmeckener', 'Mulligaturizatinglers', 'Assumphandships', 'Shoshopliancemeter', 'Assurabilist', 'Cabiliariest', 'Bonaticialissimulativers', 'Verablutivelers', 'Cabalivators', 'Orcemendarience', 'Cabalitartraitiner', 'Orcemetrivanish', 'Orcemetrigly', 'Zoopatrimatuatitis', 'Mulgatecrack', 'Orcemetrived', 'Glacionablenter', 'Trajectionaturationshine', 'Zoopatrollabify', 'Unaccenteringeminactionless', 'Mullighthawkwarrantly', 'Zoopatrilinishment', 'Cabiliarists', 'Unaccessifictionablengthene', 'Dressionistimatutilithographic', 'Bonaticasser', 'Cabalinaturationingfully', 'Verbifurcatigraveyancier', 'Mulatosphere', 'Shortwaverounds', 'Verbifurcatient', 'Zoopatrilizational', 'Mulgatorizingly', 'Shoshopriceling']

certs={
	'NR':'',
	'G':' is rated G. All ages admitted. Nothing that would offend parents for viewing by children.',
	'PG-13':' is rated PG-13. Some material may be inappropriate for children under 13 or preteenagers. Parents are urged to accompany preteenagers.',
	'R':' is rated R. Individuals under 17 require an accompanying parent or adult guardian. Contains some adult material. Parents are urged to learn more about the film before taking their young children with them.',
	'NC-17':' is rated NC-17. No one 17 and under admitted. Clearly adult. Children are not admitted.',
	'PG':' is rated PG. Some material may not be suitable for children. Parents urged to give "parental guidance". May contain some material parents might not like for their young children.'
}

tcerts={
	'NR':'',
	'TV-Y':' is rated TV-Y. It is designed to be appropriate for all children.',
	'TV-Y7':' is rated TV-Y7. It is designed for children age 7 and above',
	'TV-G':' is rated TV-G. It is suitable for all ages.',
	'TV-PG':' is rated TV-PG. It contains material that parents may find unsuitable for younger children',
	'TV-14':' is rated TV-14. It contains some material that many parents would find unsuitable for children under 14 years of age',
	'TV-MA':' is rated TV-MA. It is specifically designed to be viewed by adults and therefore may be unsuitable for children under 17.'

}

def about(request):
	return render(request, 'writers_block/about.html')

'''
def index(request):
	blocks=Block.objects.all().order_by('-posted_on')
	page = request.GET.get('page', 1)
	paginator = Paginator(blocks, 10)
	
	try:
		block_list = paginator.page(page)
	except PageNotAnInteger:
		block_list = paginator.page(1)
	except EmptyPage:
		block_list = paginator.page(paginator.num_pages)

	context={
	'block_form':Block_form(),
	'comment_form':Comment_form(),
	'pieces':Piece.objects.filter(visibility=True).order_by('-created_on')[:10],
	'block_list':block_list,
	'request': request
	}

	return render(request, 'writers_block/index.html', context)
'''

def index2(request):
	p=requests.get('https://api.themoviedb.org/3/movie/upcoming?api_key=4ce570b5135503d520df426d7989073f&language=en-US&page=1')
	m=requests.get('https://api.themoviedb.org/3/tv/popular?api_key=4ce570b5135503d520df426d7989073f&language=en-US&page=1')
	movies=json.loads(p.text)
	tvs=json.loads(m.text)
	return render(request, 'writers_block/index2.html', {'movies':movies, 'tvs':tvs})

def movie_detail(request, movie_id):
	m=Movie.objects.get_or_create(movie_id=movie_id)[0]
	if not 'can_delete_block' in request.session.keys():
		request.session['can_delete_block']=[]
	blocks=Anon_block.objects.filter(movie=m).order_by('-posted_on')
	
	p=requests.get('https://api.themoviedb.org/3/movie/'+movie_id+'?api_key=4ce570b5135503d520df426d7989073f&append_to_response=release_dates,credits,videos,images,recommendations')
	movie=json.loads(p.content.decode('utf-8'))

	context={'comment_form':Comment_form(),'block_form':Mblock_form(),'block_list':blocks, 'movie':movie, 'm_js':p.content.decode('utf-8'), 'addy':[3,10,20,27]}

	cert=None
	for i in movie['release_dates']['results']:
		if i["iso_3166_1"]=='US':
			cert=i['release_dates'][0]['certification']
	if not cert:
		cert='NR'

	try: 
		context['cert']=certs[cert]
	except:
		context['cert']=''



	context['main_vid'], context['yoblocks']=None, None
	if movie['videos']['results']:
		context['main_vid']=movie['videos']['results'][0]['key']
		context['yoblocks']=[]
		for i in movie['videos']['results']:
			yo=requests.get('https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&videoId='+context['main_vid']+'&key=AIzaSyAHWlsuk6CrUZW9zADaEf71dGTDSoefCrk&order=relevance&maxResults=30')
			p=json.loads(yo.text)
			if 'items' in p.keys():
				for i in p['items']:
					if len(context['yoblocks'])==30:
						break
					i['screen_name']=random_auths[randint(0,200)]
					i['profile_pic']=STATIC_URL+'monsters/'+str(randint(1,30))+'.png'
					formatt = "%Y-%m-%d"
					i['time']= datetime.datetime.strptime(i['snippet']['topLevelComment']['snippet']['updatedAt'][:10], formatt)
					context['yoblocks'].append(i)
	else:
		context['main_vid']=None
	

	return render(request, 'writers_block/movie_detail.html', context)

def follow_movie(request, movie_id):
	print(movie_id)
	movie=get_object_or_404(Movie, movie_id=int(movie_id))
	movie.followers.add(request.user)
	return HttpResponse()

def unfollow_movie(request, movie_id):
	movie=get_object_or_404(Movie, movie_id=int(movie_id))
	movie.followers.remove(request.user)
	return HttpResponse()

def tv_detail(request, tv_id):
	t=TV.objects.get_or_create(tv_id=tv_id)[0]
	blocks=blocks=Anon_block.objects.filter(tv=t).order_by('-posted_on')

	p=requests.get('https://api.themoviedb.org/3/tv/'+tv_id+'?api_key=4ce570b5135503d520df426d7989073f&append_to_response=credits,videos,images,similar,content_ratings,external_ids')
	tv=json.loads(p.content.decode('utf-8'))

	try:
		tv_lang=langs[tv['original_language']]
	except KeyError:
		tv_lang=None
	context={'comment_form':Comment_form(),'block_form':Mblock_form(),'block_list':blocks, 'tv':tv, 'tv_lang':tv_lang, 't_js':p.content.decode('utf-8'), 'addy':[3,10,20,27]}
	
	cert=None
	for i in tv['content_ratings']['results']:
		if i["iso_3166_1"]=='US':
			cert=i['rating']
	if not cert:
		cert='NR'

	context['cert']=tcerts[cert]	

	if tv['videos']['results']:
		context['main_vid']=tv['videos']['results'][0]['key']
		context['yoblocks']=[]
		for i in tv['videos']['results']:
			yo=requests.get('https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&videoId='+context['main_vid']+'&key=AIzaSyAHWlsuk6CrUZW9zADaEf71dGTDSoefCrk&order=relevance&maxResults=30')
			p=json.loads(yo.text)
			if 'items' in p.keys():
				for i in p['items']:
					if len(context['yoblocks'])==25:
						break
					i['screen_name']=random_auths[randint(0,200)]
					i['profile_pic']=STATIC_URL+'monsters/'+str(randint(1,30))+'.png'
					formatt = "%Y-%m-%d"
					i['time']= datetime.datetime.strptime(i['snippet']['topLevelComment']['snippet']['updatedAt'][:10], formatt)
					context['yoblocks'].append(i)
	else:
		context['main_vid']=None

	return render(request, 'writers_block/tv_detail.html', context)

def rate_movie(request,movie_id):
	if 'guest_id' not in request.session.keys():
		g=requests.get('https://api.themoviedb.org/3/authentication/guest_session/new?api_key=4ce570b5135503d520df426d7989073f')
	g=json.loads(g.text)['guest_session_id']
	url = "https://api.themoviedb.org/3/movie/421638/rating"
	payload = "{\"value\":7}"
	headers = {'content-type': 'application/json;charset=utf-8'}
	response = requests.request("POST", url, data=payload, headers=headers)
	if json.loads(response.text)['status_code']==1:
		return JsonResponse({'Success':True})
	else:
		return JsonResponse({'Success':False})




def person_detail(request, person_id):
	c=Celeb.objects.get_or_create(celeb_id=person_id)[0]
	p=requests.get('https://api.themoviedb.org/3/person/'+person_id+'?api_key=4ce570b5135503d520df426d7989073f&append_to_response=images')
	c=p.text
	person=json.loads(c)
	context={'person':person, 'p_js':c}

	return render(request, 'writers_block/person_detail.html', context)



'''
def write_movie_block(request, movie_id):
	if not request.user.is_authenticated:
		return redirect('/users/signin/?next=/index/md/'+movie_id)
	if request.method=='POST':
		form=Mblock_form(request.POST, request.FILES)
		if form.is_valid():
			f=form.cleaned_data
			movie=Movie.objects.get_or_create(movie_id=movie_id)[0]
			new_block=Block(content=f['content'], author=request.user, image=f['image'])
			new_block.post_it()
			new_block.movie=movie
			new_block.save(update_fields=["movie"])
	return redirect(reverse('movie_detail', kwargs={'movie_id':movie_id}))
			

def write_tv_block(request, tv_id):
	if not request.user.is_authenticated:
		return redirect('/users/signin/?next=/index/td/'+tv_id)
	if request.method=='POST':
		form=Mblock_form(request.POST, request.FILES)
		if form.is_valid():
			f=form.cleaned_data
			tv=TV.objects.get_or_create(tv_id=tv_id)[0]
			new_block=Block(content=f['content'], author=request.user, image=f['image'])
			new_block.post_it()
			new_block.tv=tv
			new_block.save(update_fields=["tv"])
	return redirect(reverse('tv_detail', kwargs={'tv_id':tv_id}))
'''



#Anonymous block code

def anon_tblock(request, tv_id):
	if request.method=='POST':
		try:
			auth=request.session['auth_name']
		except KeyError:
			request.session['auth_name']=random_auths[randint(0,200)]
			auth=request.session['auth_name']
		form=Mblock_form(request.POST, request.FILES)
		if form.is_valid():
			ip = get_ip(request)
			if ip is not None:
				ip_hash=md5(ip.encode()).hexdigest()
			else:
				ip_hash='8fcc6c61d0b597cf5b8ade2722062a2e5'
				ip='0.0.0.0'
			f=form.cleaned_data
			tv=TV.objects.get_or_create(tv_id=tv_id)[0]
			new_block=Anon_block(content=f['content'], auth_name=auth, image=f['image'], profile=ip_hash, ip=ip)
			new_block.post_it()
			new_block.tv=tv
			new_block.save(update_fields=["tv"])
			request.session['can_delete_block'].append(new_block.id)
			request.session.modified = True
	return redirect(reverse('tv_detail', kwargs={'tv_id':tv_id}))

def anon_mblock(request, movie_id):
	if request.method=='POST':
		form=Mblock_form(request.POST, request.FILES)
		try:
			auth=request.session['auth_name']
		except KeyError:
			request.session['auth_name']=random_auths[randint(0,200)]
			auth=request.session['auth_name']
		if form.is_valid():
			ip = get_ip(request)

			if ip is not None:
				ip_hash=md5(ip.encode()).hexdigest()
			else:
				ip_hash='8fcc6c61d0b597cf5b8ade2722062a2e5'
				ip='0.0.0.0'
			f=form.cleaned_data
			movie=Movie.objects.get_or_create(movie_id=movie_id)[0]
			new_block=Anon_block(content=f['content'], auth_name=auth, image=f['image'], profile=ip_hash, ip=ip)
			new_block.post_it()
			new_block.movie=movie
			new_block.save(update_fields=["movie"])
			request.session['can_delete_block'].append(new_block.id)
			request.session.modified = True
	return redirect(reverse('movie_detail', kwargs={'movie_id':movie_id}))


def delete_anon_block(request):
	if request.method=='POST':
		block_id=request.POST.get('block_id')
		block=get_object_or_404(Anon_block,pk=int(block_id))
		if block.id in request.session['can_delete_block']:
			block.delete()
			data={'block_id':block_id}
	return JsonResponse(data)

def like_anon_block(request):
	if request.method=='POST':
		block=get_object_or_404(Anon_block, pk=int(request.POST.get('block_id', None)))
		if request.POST.get('like')=='1':
			block.likes+=1
		else:
			block.likes-=1
		block.save()
	return HttpResponse('')

def write_anon_comment(request):
	if request.method=='POST':
		ip = get_ip(request)
		if ip is not None:
			ip_hash=md5(ip.encode()).hexdigest()
		else:
			ip_hash='8fcc6c61d0b597cf5b8ade2722062a2e5'
		block_id=request.POST.get('block_id', None)
		block=get_object_or_404(Anon_block, pk=int(block_id))
		new_comment=Anon_comment(rant=request.POST.get('text'), block=block, profile=ip_hash)
		new_comment.post_it()
		request.session['can_delete_com'].append(new_comment.id)
		request.session.modified = True
		comment={'rant':new_comment.rant,       
		'count': block.comments.count(),
		'id':new_comment.id,
		'num': block.comments.count(),
		}
		data={'comment': comment}
		return JsonResponse(data)

def delete_anon_comment(request):
	if request.method=='POST':
		c=get_object_or_404(Anon_comment, pk=int(request.POST.get('cid')))
		if c.id in request.session['can_delete_com']:
			c.delete()
	return HttpResponse('')

def upvote_anon_comment(request):
	if request.method=='POST':
		c=get_object_or_404(Anon_comment, pk=int(request.POST.get('cid')))
		if request.POST.get('like')=='1':
			c.upvotes+=1
		else:
			c.upvotes-=1
		c.save()
	return HttpResponse('')

		

# End of anonymous block code


'''

@login_required
def delete_block(request):
	if request.method=='POST':
		block_id=request.POST.get('block_id')
		block=get_object_or_404(Block,pk=int(block_id))
		block.delete()
		data={'block_id':block_id}
		return JsonResponse(data)


def write_comment(request):
	if request.user.is_authenticated():
		if request.method=='POST':
			block_id=request.POST.get('block_id', None)
			block=get_object_or_404(Block, pk=int(block_id))
			new_comment=Comment(rant=request.POST.get('text'), block=block, user=request.user)
			new_comment.post_it()
			Notification.objects.create(from_user=request.user,
				to_user=block.author,
				not_type='C',
				block=block,
				)
			comment={'rant':new_comment.rant, 
			'user': new_comment.user.id, 
			'image_url': request.user.person.thumbnail.url, 
			'count': block.comments.count(),
			'id':new_comment.id,
			'profile':reverse('profile_view', kwargs={'pk':new_comment.user.id}),
			'num': block.comments.count(),
			'logged_in':True
			}
			data={'comment': comment}
			return JsonResponse(data)
	else:
		return JsonResponse({'comment':{'logged_in':False}})


@login_required
def delete_comment(request):
	if request.method=='POST':
		c=get_object_or_404(Comment, pk=int(request.POST.get('cid')))
		c.delete()
		return HttpResponse('')

@login_required
def up_com(request):
	if request.method=='POST':
		c=get_object_or_404(Comment, pk=int(request.POST.get('cid')))
		if request.user in c.upvotes.all():
			c.upvotes.remove(request.user)
		else:
			c.upvotes.add(request.user)
	return HttpResponse('')


@login_required
def like_block(request):
	if request.method=='POST':
		block_id=request.POST.get('block_id', None)
		block=get_object_or_404(Block, pk=int(block_id))
		if request.user not in block.likes.all():
			request.user.liked.add(block)
			if request.user!=block.author:
				Notification.objects.create(from_user=request.user,
				to_user=block.author,
				not_type='L',
				block=block)
		else:
			Notification.objects.filter(from_user=request.user,
			to_user=block.author,
			not_type='L',
			block=block,).delete()
			block.likes.remove(request.user)
		return HttpResponse('')

'''

def bingxml(request):
	return HttpResponse(open(STATIC_ROOT+'/BingSiteAuth.xml').read())

def block_view(request, block_id):
	blocky=get_object_or_404(Anon_block, pk=block_id)
	return render(request, 'writers_block/block_view.html', {'blocky':blocky})


def subscribe(request):
	if request.method=='POST':
		email=request.POST.get('email')
		if User.objects.filter(email=email).exists():
			return JsonResponse({'msg':'You Are Already A Subscriber!'})
		else:
			u=User.objects.create(email=email, username=email)
			return JsonResponse({'msg':'Successfully Subscribed!'})


def artwork(request):
	return render(request, 'writers_block/artwork.html', {'form':Fanart_form, 'alert':None})

def submit_fanart(request):
	if request.method=='POST':
		form=Fanart_form(request.POST)
		if form.is_valid():
			p=form.cleaned_data
			u=User.objects.get_or_create(username=p['email'], email=p['email'])
			if p['topic_type']=='movie':
				m=Movie.objects.get_or_create(movie_id=p['topic_id'])
			else:
				m=TV.objects.get_or_create(tv_id=p['topic_id'])
			art=p['img']
			f=Fanart.objects.create(piece=art)
			f.save()
			m[0].fanart.add(f)
			
			subject = 'FanArt Submission'
			html_message= render_to_string('writers_block/fanart_mail.html', {'user': p['name']})
			message='We recieved your Fan Art link submission. This email is to inform you that we\'ll send you a confirmation and features your link on ReelBugs as soon as we review it\'s authenticity. It\'ll just take 1-2 days.'
			from_email = 'ReelBugs Support <vaish@reelbugs.com>'
			recipient_list = [p['email'],]
			send_mail(subject=subject, message=message, html_message=html_message, from_email=from_email, recipient_list=recipient_list)

			return render(request, 'writers_block/artwork.html', {'alert':'Submission was successful! You will recieve a mail from us.'})
		else:
			return render(request, 'writers_block/artwork.html', {'alert':'Submission was unsuccessful!'})
	return redirect('artwork')




