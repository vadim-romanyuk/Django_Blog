from django import forms
from ckeditor.widgets import CKEditorWidget



class PostCreateForm(forms.Form):
	title = forms.CharField(label='Заголовок', required=True)
	content = forms.CharField(label='Содержание', required=True, localize=True, widget=forms.Textarea)
	email = forms.DecimalField(label='Сумма', required=True, max_digits=4)
	image = forms.ImageField(required=False)
