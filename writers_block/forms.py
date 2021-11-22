from django import forms
from .models import Anon_block, Anon_comment

class Block_form(forms.Form):
	content=forms.CharField(widget=forms.Textarea(attrs={'placeholder': "What's up?",'class' : 'form-control', 'rows':'6', 'cols':'60'}))
	image=forms.ImageField(required=False)
	movie_id=forms.CharField(widget=forms.HiddenInput(attrs={'class':'b_movid'}))


class Mblock_form(forms.Form):
	content=forms.CharField(widget=forms.Textarea(attrs={'placeholder': "What's up?",'class' : 'form-control', 'rows':'6', 'cols':'60'}))
	image=forms.ImageField(required=False)


class Comment_form(forms.ModelForm):
	class Meta:
		model=Anon_comment
		fields=['rant']


class Fanart_form(forms.Form):
	email=forms.EmailField()
	img=forms.URLField()
	topic_id=forms.CharField()
	topic_type=forms.CharField()
