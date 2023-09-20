from django.template.loader import render_to_string
from django.core.mail.message import EmailMultiAlternatives
from django.conf import settings

def get_subscriber(category):
  user_email = []
  for user in category.subscribes.all():
    user_email.append(user.email)
  return user_email


def news_post_subscription(instance):
  template = 'mail/new_post.html'

  for category in instance.category.all():
    email_subject = f'New post in category "{category}"!'
    user_emails = get_subscriber(category)

    html = render_to_string(
        remplate_name = template,
        cantext={
          'category' : category,
          'post' : instance.post,
        },
      )
    msg = EmailMultiAlternatives(
        subject=email_subject,
        body='',
        from_email=settings.DEFAULT_FROM_MAIL,
        to=user_emails
      )
    msg.attach_alternative(html, 'text/html')
    msg.send()