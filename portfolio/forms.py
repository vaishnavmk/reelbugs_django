from django import forms
from .models import Piece

class WritePiece_Form(forms.Form):
	content=forms.CharField(widget=forms.Textarea())

class CreatePiece_Form(forms.Form):
	title=forms.CharField()
	thumb=forms.ImageField()
	summary=forms.CharField(required=False)

class EditPiece_Form(forms.Form):
	title=forms.CharField()
	thumb=forms.ImageField(required=False)



