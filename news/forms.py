from django.forms import ModelForm
from .models import Post
from django import forms
from .models import Author

class PostForm(ModelForm):
    #def __init__(self, *args, **kwargs):
    #    super().__init__(*args, **kwargs)
    #    self.fields['author'].widget = forms.HiddenInput()

    class Meta:
        model = Post
        fields = ['title', 'text', 'category']
        widgets = {
            'title' : forms.TextInput(attrs={
                  'class' : 'form-control',
                  'palaceholder' : 'Заголовок...',
                  'id' : 'postform-title-field'
                }),
            'text' : forms.Textarea(attrs={
                  'class' : 'form-control',
                  'id' : 'postform-text-field'
                }),
            'category' : forms.SelectMultiple(attrs={
                  'class' : 'form-control', 
                  'id' : 'postform-category-field'
                })
        }