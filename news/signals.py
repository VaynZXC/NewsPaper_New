from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from news.models import PostCategory
import threading

from news.tasks import new_post_subscription

@receiver(m2m_changed, sender = PostCategory)
def notify_subscribers(sender, instance, **kwargs):
  if kwargs['action'] == 'post_add':
    new_post_subscription(instance)
    
def notify_subscribers_next_week():
  timer = threading.Timer(604800, notify_subscribers) #таймер на 1 неделю