from django import template
 
register = template.Library()

@register.filter(name='censor')

def censor(value):
    words = ['политики']
    split_str = value.split()
    for word in words:
      if word in value:
          value = 'В статье есть запрещённые слова. Доступ закрыт!'
          return str(value)
      else:
          return ' '.join((filter(lambda s: s not in words, split_str)))