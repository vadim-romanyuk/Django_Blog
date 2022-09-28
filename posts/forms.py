from django import forms
from ckeditor.widgets import CKEditorWidget
from posts.serializers import PostSerializer
from .models import Post


class PostCreateForm(forms.Form):
	title = forms.CharField(label='Заголовок', required=True)
	image = forms.ImageField(required=False)
	content = forms.CharField(label='Содержание', required=True, localize=True, widget=CKEditorWidget)
	# email = forms.DecimalField(label='Сумма', required=True, max_digits=4)


class PostModelForms(forms.ModelForm):
	class Meta:
		model = Post
		fields = '__all__'
		exclude = ['user']

