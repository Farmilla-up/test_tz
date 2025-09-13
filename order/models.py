from django.db import models

from django.db import models

class Category(models.Model):
    """
    Модель категорий продуктов.

    Поля:
    - name: название категории.
    - parent: родительская категория (для иерархии).
    - root_category: верхняя категория в иерархии (для ускоренной агрегации).

    Связи:
    - children: дочерние категории (обратная связь для parent).
    - rooted: все категории, у которых эта категория является корнем.
    """
    name = models.CharField(max_length=255)
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="children",
        help_text="Родительская категория для иерархии"
    )
    root_category = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="rooted",
        help_text="Верхняя категория для ускоренной агрегации"
    )


class Product(models.Model):
    """
    Модель продуктов.

    Поля:
    - name: название продукта.
    - quantity: текущее количество на складе.
    - price: цена продукта.
    - category: категория продукта.
    """
    name = models.CharField(max_length=255, help_text="Название продукта")
    quantity = models.PositiveIntegerField(help_text="Количество на складе")
    price = models.DecimalField(max_digits=12, decimal_places=2, help_text="Цена продукта")
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        help_text="Категория продукта"
    )


class Customer(models.Model):
    """
    Модель клиентов.

    Поля:
    - name: имя клиента.
    - address: адрес клиента.
    """
    name = models.CharField(max_length=255, help_text="Имя клиента")
    address = models.TextField(help_text="Адрес клиента")


class CustomerOrder(models.Model):
    """
    Модель заказов клиентов.

    Поля:
    - customer: клиент, который сделал заказ.
    - order_date: дата и время создания заказа (автоустановлено).
    """
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        help_text="Клиент, который сделал заказ"
    )
    order_date = models.DateTimeField(
        auto_now_add=True,
        help_text="Дата и время создания заказа"
    )


class OrderItem(models.Model):
    """
    Модель элементов заказа (позиции заказа).

    Поля:
    - order: заказ, к которому относится позиция.
    - product: продукт, который был заказан.
    - quantity: количество продукта в заказе.
    - price: цена продукта на момент заказа.
    """
    order = models.ForeignKey(
        CustomerOrder,
        on_delete=models.CASCADE,
        help_text="Заказ, к которому относится позиция"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        help_text="Продукт, который был заказан"
    )
    quantity = models.PositiveIntegerField(help_text="Количество продукта в заказе")
    price = models.DecimalField(max_digits=12, decimal_places=2, help_text="Цена продукта на момент заказа")
