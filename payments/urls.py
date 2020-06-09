from django.urls import path
from .views import (
    CheckoutView,
    PaymentView,
    AddCouponView,
)

app_name = 'payments'

urlpatterns = [
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('add-coupon/', AddCouponView.as_view(), name='add-coupon'),
    path('payment/<payment_option>/', PaymentView.as_view(), name='payment'),
]