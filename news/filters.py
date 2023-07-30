from django_filters import FilterSet, ChoiceFilter
from .models import Post, Category


class PostFilter(FilterSet):
    cat = ChoiceFilter(field_name='category__category', choices=Category.THEMES, label='Поиск по категории')
    class Meta:
        model = Post
        fields = ('title', 'time_in', 'post_rating', 'author')