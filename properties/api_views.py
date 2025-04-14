from rest_framework import generics
from .models import Property, Reservation
from .serializers import ReservationSerializer
from .serializers import PropertySerializer

class PropertyListCreateAPIView(generics.ListCreateAPIView):
    queryset = Property.objects.all().order_by('-created_at')
    serializer_class = PropertySerializer

class ReservationListCreateAPIView(generics.ListCreateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
