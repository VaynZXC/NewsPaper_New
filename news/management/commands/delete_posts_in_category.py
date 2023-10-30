from django.core.management.base import BaseCommand, CommandError
from news.models import Category, Post

class Command(BaseCommand):
  help = 'Удаляет все посты из выбранной ккатегории'
  missing_args_message = 'Недостаточно аргументов'
  requires_migrations_checks = True

  def add_arguments(self, parser):
    parser.add_argument('category', type=str)
  
  def handle(self, *args, **options):
    self.stdout.readable()
    answer =  input(f'Вы действительно хотите удалить все посты из категории {options["category"]}? yes/no')

    if answer != 'yes':
        self.stdout.write(self.style.ERROR('Отказано в доступе'))
                            # sport = 'SP'
                            # politics = 'PO'
                            # education = 'ED'
                            # leisure = 'LE'
    try:
        category = Category.objects.get(category = options['category'])
        Post.objects.filter(category = category).delete()
        self.stdout.write(self.style.SUCCESS(f'Посты из категории {category} удалены'))
    except Post.DoesNotExist:
        self.stdout.write(self.style.ERROR('Категория не найдена'))
