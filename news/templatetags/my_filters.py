from django import template
 
register = template.Library()

@register.filter(name='censor')

def censor(value):
    words = ['политики']
    value= str()
    for word in words:
      if value.find(word) != -1:
          value = 'В статье есть запрещённые слова. Доступ закрыт!'
          return str(value)
      else:
          return str(value)