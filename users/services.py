from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from users.token import account_activation_token


def get_vrification(request, user):
    user.is_active = False
    user.save()

    # Получение текущего сайта
    current_site = get_current_site(request)

    # Подготовка данных для отправки электронного письма

    mail_subject = 'Теперь вы зарегистрированы на нашем сервисе! Подтвердите свой электронный адрес.'
    message = render_to_string('users/acc_active_email.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
    })
    to_email = user.email
    email = EmailMessage(
        mail_subject, message, to=[to_email]
    )
    email.send()
