from django import forms
from .models import Post

class PostForm(forms.ModelForm):
	publish = forms.DateField(widget=forms.SelectDateWidget(years=range(2020, 1980, -1)))
	class Meta:
		model = Post
		fields = [              #creates form with title and content fields
			"title",
			"content",
			"image",
			"draft",
			"publish",
		]