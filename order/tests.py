from django.test import TestCase
import pytest
from django.urls import reverse
from rest_framework import status
from .models import Customer, CustomerOrder, Product, OrderItem, Category
from rest_framework.test import APIClient

@pytest.mark.django_db
def test_add_item_success(client):
    customer = Customer.objects.create(name="Test", address="Addr")
    order = CustomerOrder.objects.create(customer=customer)

    category = Category.objects.create(name="Phones")
    product = Product.objects.create(name="Phone", quantity=5, price=100, category=category)

    url = reverse("add-item", kwargs={"order_id": order.id})
    response = client.post(url, {"product_id": product.id, "quantity": 2}, format="json")

    assert response.status_code == status.HTTP_200_OK
    assert OrderItem.objects.count() == 1
    product.refresh_from_db()
    assert product.quantity == 3


@pytest.mark.django_db
def test_add_item_not_enough_stock(client):
    customer = Customer.objects.create(name="Test", address="Addr")
    order = CustomerOrder.objects.create(customer=customer)

    category = Category.objects.create(name="Phones")
    product = Product.objects.create(name="Phone", quantity=1, price=100, category=category)

    url = reverse("add-item", kwargs={"order_id": order.id})
    response = client.post(url, {"product_id": product.id, "quantity": 5}, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "not enough stock" in response.json()["error"]


@pytest.mark.django_db
def test_add_item_invalid_product(client):
    customer = Customer.objects.create(name="Test", address="Addr")
    order = CustomerOrder.objects.create(customer=customer)

    url = reverse("add-item", kwargs={"order_id": order.id})
    response = client.post(url, {"product_id": 999, "quantity": 1}, format="json")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "no such product" in response.json()["error"]