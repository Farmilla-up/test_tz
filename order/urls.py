from django.urls import path
from .views import AddItemView

urlpatterns = [
    path("<int:order_id>/add_item/", AddItemView.as_view(), name="add-item"),
]