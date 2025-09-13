import os
import django
from decimal import Decimal

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "test_tz.settings")
django.setup()

from order.models import Category, Product, Customer, CustomerOrder, OrderItem


Category.objects.all().delete()
Product.objects.all().delete()
Customer.objects.all().delete()
CustomerOrder.objects.all().delete()
OrderItem.objects.all().delete()

# --- Категории ---
electronics = Category.objects.create(id=1, name="Electronics")
phones = Category.objects.create(id=2, name="Phones", parent=electronics, root_category=electronics)
laptops = Category.objects.create(id=3, name="Laptops", parent=electronics, root_category=electronics)

home = Category.objects.create(id=4, name="Home Appliances")
kitchen = Category.objects.create(id=5, name="Kitchen", parent=home, root_category=home)
cleaning = Category.objects.create(id=6, name="Cleaning", parent=home, root_category=home)

toys = Category.objects.create(id=7, name="Toys")
lego = Category.objects.create(id=8, name="LEGO", parent=toys, root_category=toys)
plush = Category.objects.create(id=9, name="Plush Toys", parent=toys, root_category=toys)

# --- Товары ---
iphone = Product.objects.create(id=1, name="iPhone", quantity=20, price=Decimal("999.99"), category=phones)
samsung = Product.objects.create(id=2, name="Samsung Galaxy", quantity=15, price=Decimal("799.99"), category=phones)
macbook = Product.objects.create(id=3, name="MacBook Pro", quantity=5, price=Decimal("1999.99"), category=laptops)
dell = Product.objects.create(id=4, name="Dell XPS", quantity=8, price=Decimal("1499.99"), category=laptops)

microwave = Product.objects.create(id=5, name="Microwave", quantity=12, price=Decimal("199.99"), category=kitchen)
blender = Product.objects.create(id=6, name="Blender", quantity=20, price=Decimal("99.99"), category=kitchen)
vacuum = Product.objects.create(id=7, name="Vacuum Cleaner", quantity=10, price=Decimal("299.99"), category=cleaning)

lego_city = Product.objects.create(id=8, name="LEGO City", quantity=30, price=Decimal("59.99"), category=lego)
lego_starwars = Product.objects.create(id=9, name="LEGO Star Wars", quantity=25, price=Decimal("119.99"), category=lego)
teddy = Product.objects.create(id=10, name="Teddy Bear", quantity=40, price=Decimal("29.99"), category=plush)

# --- Клиенты ---
alice = Customer.objects.create(id=1, name="Alice", address="Some street 1")
bob = Customer.objects.create(id=2, name="Bob", address="Another street 2")
charlie = Customer.objects.create(id=3, name="Charlie", address="Third street 3")
diana = Customer.objects.create(id=4, name="Diana", address="Fourth street 4")

# --- Заказы ---
order1 = CustomerOrder.objects.create(id=1, customer=alice)
order2 = CustomerOrder.objects.create(id=2, customer=bob)
order3 = CustomerOrder.objects.create(id=3, customer=charlie)
order4 = CustomerOrder.objects.create(id=4, customer=alice)
order5 = CustomerOrder.objects.create(id=5, customer=diana)

# --- Позиции заказов ---
OrderItem.objects.create(id=1, order=order1, product=iphone, quantity=2, price=iphone.price)
OrderItem.objects.create(id=2, order=order1, product=macbook, quantity=1, price=macbook.price)

OrderItem.objects.create(id=3, order=order2, product=samsung, quantity=3, price=samsung.price)
OrderItem.objects.create(id=4, order=order2, product=vacuum, quantity=1, price=vacuum.price)

OrderItem.objects.create(id=5, order=order3, product=lego_city, quantity=5, price=lego_city.price)
OrderItem.objects.create(id=6, order=order3, product=teddy, quantity=2, price=teddy.price)

OrderItem.objects.create(id=7, order=order4, product=blender, quantity=3, price=blender.price)
OrderItem.objects.create(id=8, order=order4, product=lego_starwars, quantity=1, price=lego_starwars.price)

OrderItem.objects.create(id=9, order=order5, product=iphone, quantity=1, price=iphone.price)
OrderItem.objects.create(id=10, order=order5, product=dell, quantity=2, price=dell.price)
