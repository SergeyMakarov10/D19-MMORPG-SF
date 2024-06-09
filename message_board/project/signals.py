from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives, mail_managers
from django.conf import settings
from .models import *
from django.contrib.auth.models import User


# отправляем сообщение автору объявления о появлении отклика
@receiver(post_save, sender=Comment)
def create_comment(sender, instance, created, **kwargs):
    if created:

        html_content = render_to_string(
            'flatpages/comment_create_email.html',
            {
                'text': f'''Пользователь {instance.comment_author.username}, откликнулся на ваше объявление: '{instance.post.title}'. ''' ,
                'link': f'''{settings.SITE_URL}{'post/'}{instance.post.id}''',
            }
        )
        msg = EmailMultiAlternatives(

            subject = 'Отклик на объявление',
            body = '',
            from_email = settings.DEFAULT_FROM_EMAIL,
            # сообщение направляем автору объявления
            to = [instance.post.post_author.email],
            )
        msg.attach_alternative(html_content, 'text/html')
        msg.send()


# отправляем сообщение автору отклика о принятии его автором объявления
@receiver(post_save, sender=Comment)
def comment_accept(sender, instance, created, **kwargs):

    if instance.status:

        html_content = render_to_string(
            'flatpages/comment_create_email.html',
            {
                'text': f'''Автор объявления {instance.post.post_author}, принял ваш отклик: '{instance.content[0:50]}'. ''',
                'link': f'''{settings.SITE_URL}{'post/'}{instance.post.id}''',
            }
        )
        msg = EmailMultiAlternatives(

            subject = 'Принятие отклика на объявление',
            body = '',
            from_email = settings.DEFAULT_FROM_EMAIL,
            # сообщение направляем авттору отклика
            to = [instance.comment_author.email],
            )
        msg.attach_alternative(html_content, 'text/html')
        msg.send()


#рассылка для подписчиков при появлении объявления
@receiver(post_save, sender=Post)

def send_email(sender, instance, created, **kwargs):
    if created:
        all_subscribers = instance.categories.subscribers.all()
        subscribers_emails = []
        for sub in all_subscribers:
            if sub != instance.post_author.id:
                subscribers_emails += [s.email for s in all_subscribers]

        html_content = render_to_string(
            'flatpages/post_created_email.html',
            {
                'text': f'''{instance.title[0:50]}: '{instance.content[0:150]}...' ''',
                'link': f'''{settings.SITE_URL}{'post/'}{instance.id}''',
            }
        )
        msg = EmailMultiAlternatives(
            subject='Создание объявления',
            body='',
            from_email=settings.DEFAULT_FROM_EMAIL,
           to=subscribers_emails,
        )
        msg.attach_alternative(html_content, 'text/html')
        msg.send()
