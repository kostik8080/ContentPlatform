import stripe
from django.conf import settings
from users.models import Subscription

stripe.api_key = settings.STRIPE_KEYS

def create_stripe_subcriptions(instance):
    new_subscription = f'подписка № {instance.id}'
    stripe_product = stripe.Product.create(
        name=new_subscription,
    )
    return stripe_product['id']


def create_stripe_price(product_id):
    """ Создает цену в Стрипе."""

    stripe_price = stripe.Price.create(
        currency="rub",
        unit_amount=1000 * 100,
        product=product_id
    )
    return stripe_price['id']


def create_stripe_session(price):
    """ Создает сессию на оплату в Стрипе."""
    session = stripe.checkout.Session.create(
        success_url='http://127.0.0.1:8000/success',
        line_items=[{"price": price, "quantity": 1}],
        mode="payment",

    )
    return session.get('id'), session.get('url')

