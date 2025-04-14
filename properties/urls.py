from django.urls import path
from . import views

app_name = 'properties'

urlpatterns = [
    path('', views.property_list, name='list'),
    path('search/', views.property_search, name='search'),
    path('<int:pk>/', views.property_detail, name='detail'),  # URL pour les détails
    path('create/', views.property_create, name='create'),
    path('<int:pk>/edit/', views.property_edit, name='edit'),
    path('<int:pk>/delete/', views.property_delete, name='delete'),
    path('<int:property_id>/contact/', views.seller_contacts, name='contact_seller'),
]
