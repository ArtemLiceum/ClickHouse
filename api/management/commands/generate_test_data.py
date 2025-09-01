import random
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from api.models import Category, Product, Tag, Customer, Order, Discount


class Command(BaseCommand):
    help = "Генерация тестовых данных"

    def handle(self, *args, **kwargs):
        categories = [
            Category.objects.get_or_create(title="Хоз. товары", defaults={"description": "Для дома"}),
            Category.objects.get_or_create(title="Электроника", defaults={"description": "Бытовая техника"}),
            Category.objects.get_or_create(title="Одежда", defaults={"description": "Летняя одежда"}),
        ]

        tags = [
            Tag.objects.get_or_create(title="Новинка", defaults={"description": "Новинка сезона"}),
            Tag.objects.get_or_create(title="Классика", defaults={"description": "Популярная модель"}),
            Tag.objects.get_or_create(title="Скидка", defaults={"description": "Уценка"}),
        ]

        products = []
        for i in range(10):
            category = random.choice(categories)[0]
            product, _ = Product.objects.get_or_create(
                title=f"Товар {i+1}",
                category=category,
                defaults={"description": "Описание товара", "price": random.randint(100, 5000)},
            )
            product.tags.set([random.choice(tags)[0] for _ in range(random.randint(1, 2))])
            products.append(product)

        customers = []
        for i in range(5):
            customer, _ = Customer.objects.get_or_create(
                login=f"user{i}",
                defaults={
                    "name": f"Имя{i}",
                    "last_name": f"Фамилия{i}",
                    "age": random.randint(18, 60),
                },
            )
            customers.append(customer)

        discounts = []
        for i in [10, 20, 30, 40, 50]:
            discount, _ = Discount.objects.get_or_create(
                is_active=True,
                amount=i,
                category=random.choice(categories)[0],
                product=random.choice(products),
            )
            discounts.append(discount)

        for _ in range(50):
            product = random.choice(products)
            customer = random.choice(customers)
            order_date = datetime.now() - timedelta(days=random.randint(0, 30))
            Order.objects.get_or_create(
                order_datetime=order_date,
                customer=customer,
                product=product,
                amount=product.price,
                discount=random.choice(discounts),
            )

        self.stdout.write(self.style.SUCCESS("Тестовые данные сгенерированы"))
