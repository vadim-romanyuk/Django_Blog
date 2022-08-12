from django import forms



class CreateForm(forms.Form):
	title = forms.CharField(label='Заголовок', required=True)
	content = forms.CharField(label='Содержание', required=True, localize=True, widget=forms.Textarea)
	email = forms.DecimalField(label='Сумма', required=True, max_digits=4)