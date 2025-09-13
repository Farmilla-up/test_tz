from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.db import transaction

from .models import Product, CustomerOrder, OrderItem
from .serializer import AddItemSerializer


class AddItemView(GenericAPIView):
    """
        Добавляет товар в заказ.

        POST-параметры:
            order_id (URL): ID заказа
            product_id (JSON): ID товара
            quantity (JSON): количество

        Логика:
            - Если товара нет — 404
            - Если недостаточно на складе — 400
            - Если товар уже в заказе — увеличивает количество
            - Иначе создаёт новую позицию
            - Списывает товар со склада

        Ответы:
            200 — успех
            400 — ошибка (недостаточно товара или другая)
            404 — заказ или товар не найден
        """
    serializer_class = AddItemSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            product_id = serializer.validated_data['product_id']
            quantity = serializer.validated_data['quantity']
            order_id = kwargs.get('order_id')

            product = Product.objects.filter(id=product_id).first()
            if not product:
                return Response({"error": "no such product"}, status=status.HTTP_404_NOT_FOUND)

            if product.quantity < quantity:
                return Response({"error": "not enough stock"}, status=status.HTTP_400_BAD_REQUEST)

            order = CustomerOrder.objects.filter(id=order_id).first()
            if not order:
                return Response({"error": "no such order"}, status=status.HTTP_404_NOT_FOUND)

            with transaction.atomic():
                item, created = OrderItem.objects.get_or_create(
                    order=order,
                    product=product,
                    defaults={"quantity": quantity, "price": product.price},
                )
                if not created:
                    item.quantity += quantity
                    item.save()

                product.quantity -= quantity
                product.save()

            return Response({"message": "item added successfully"}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
