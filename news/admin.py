from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Post)
admin.site.register(Author)
admin.site.register(PostCategory)
admin.site.register(Category)
admin.site.register(Comment)