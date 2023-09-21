from django.forms import ModelForm
from .models import Post
from django import forms
from .models import Author

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text', 'category', 'subscribe']
        widgets = {
            'title' : forms.TextInput(attrs={
                  'class' : 'form-control',
                  'placeholder' : 'Заголовок...',
                  'id' : 'postform-title-field'
                }),
            'text' : forms.Textarea(attrs={
                  'class' : 'form-control',
                  'id' : 'postform-text-field'
                }),
            'category' : forms.SelectMultiple(attrs={
                  'class' : 'form-control', 
                  'id' : 'postform-category-field'
                }),
        }