from django.core.management.base import BaseCommand
from api.ch_service import ch_client, order_to_row
from api.models import Order

CH_BATCH = 100

class Command(BaseCommand):
    help = "Перенос заказов в ClickHouse"

    def handle(self, *args, **kwargs):
        client = ch_client()

        qs = (
            Order.objects.select_related('customer', 'product__category')
            .prefetch_related('product__tags')
            .order_by('order_datetime')
        )

        columns = [
            'order_id',
            'order_datetime',
            'customer_id',
            'customer_login',
            'customer_name',
            'customer_last_name',
            'customer_age',
            'product_id',
            'product_title',
            'product_category_id',
            'product_category_title',
            'product_tags',
            'amount',
            'discount',
            'total_price',
            'version',
        ]

        batch = []
        for order in qs.iterator(chunk_size=CH_BATCH):
            row = order_to_row(order)
            batch.append([row[col] for col in columns])

            if len(batch) >= CH_BATCH:
                client.insert('orders_for_analytics', batch, column_names=columns)
                batch = []

        if batch:
            client.insert('orders_for_analytics', batch, column_names=columns)

        self.stdout.write(self.style.SUCCESS("Заказы успешно перенесены в ClickHouse"))
