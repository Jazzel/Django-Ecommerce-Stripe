from django.urls import path
from .views import (
    ItemDetailView,
)

app_name = 'items'

urlpatterns = [
    path('product/<slug>/', ItemDetailView.as_view(), name='product'),
]