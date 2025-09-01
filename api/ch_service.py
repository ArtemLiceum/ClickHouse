from django.core.management.base import BaseCommand
from django.utils import timezone
from clickhouse_connect import get_client
from datetime import datetime, timedelta
from django.conf import settings
from .models import Order

CH_BATCH = 1000


def ch_client():
    return get_client(
        host=settings.CLICKHOUSE['HOST'],
        port=settings.CLICKHOUSE.get('PORT', 8123),
        username=settings.CLICKHOUSE.get('USER'),
        password=settings.CLICKHOUSE.get('PASSWORD'),
        database=settings.CLICKHOUSE.get('DATABASE')
    )


def order_to_row(order):
    product = order.product
    customer = order.customer
    tags = list(product.tags.values_list('title', flat=True))
    return {
        'order_id': str(order.id),
        'order_datetime': order.order_datetime,
        'customer_id': customer.id if customer else None,
        'customer_login': customer.login if customer else '',
        'customer_name': customer.name if customer else '',
        'customer_last_name': customer.last_name if customer else '',
        'customer_age': customer.age,
        'product_id': product.id,
        'product_title': product.title,
        'product_category_id': product.category.id if product.category else None,
        'product_category_title': product.category.title if product.category else '',
        'product_tags': tags,
        'amount': order.amount,
        'discount': order.discount.amount,
        'total_price': order.amount - order.discount.amount,
        'version': int(order.order_datetime.timestamp()),
    }
