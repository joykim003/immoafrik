from .api_views import ReservationListCreateAPIView
from django.urls import path
from .api_views import PropertyListCreateAPIView

urlpatterns = [
    path('biens/', PropertyListCreateAPIView.as_view(), name='api-properties'),

    path('reservations/', ReservationListCreateAPIView.as_view(), name='api-reservations'),
]
