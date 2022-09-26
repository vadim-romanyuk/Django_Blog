from django import forms
from ckeditor.widgets import CKEditorWidget


class PostCreateForm(forms.Form):
	title = forms.CharField(label='Заголовок', required=True)
	image = forms.ImageField(required=False)
	content = forms.CharField(label='Содержание', required=True, localize=True, widget=CKEditorWidget)
	# email = forms.DecimalField(label='Сумма', required=True, max_digits=4)

