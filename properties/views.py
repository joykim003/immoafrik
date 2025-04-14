# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .models import Property
from .forms import PropertyForm

from .forms import ReservationForm
from .models import Reservation
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .forms import PropertySearchForm
from django.contrib import messages

def property_list(request):
    properties = Property.objects.all().order_by('-created_at')
    return render(request, 'properties/list.html', {'properties': properties})

@login_required
def property_create(request):
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            property = form.save(commit=False)
            property.seller = request.user
            property.save()
            messages.success(request, 'Propriété créée avec succès!')
            return redirect('users:dashboard')
        else:
            messages.error(request, 'Erreur lors de la création de la propriété.')
    else:
        form = PropertyForm()
    
    return render(request, 'properties/property_form.html', {'form': form})

@login_required
def property_edit(request, pk):
    property = get_object_or_404(Property, pk=pk, seller=request.user)
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES, instance=property)
        if form.is_valid():
            form.save()
            messages.success(request, 'Propriété mise à jour avec succès!')
            return redirect('users:dashboard')
    else:
        form = PropertyForm(instance=property)
    
    return render(request, 'properties/property_form.html', {'form': form})

@login_required
def property_delete(request, pk):
    property = get_object_or_404(Property, pk=pk, seller=request.user)
    property.delete()
    messages.success(request, 'Propriété supprimée avec succès!')
    return redirect('users:dashboard')

@login_required
def create_reservation(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user = request.user
            reservation.save()
            return redirect('properties:list')
    else:
        form = ReservationForm()
    return render(request, 'properties/create_reservation.html', {'form': form})


@login_required
def dashboard(request):
    user = request.user
    reservations = Reservation.objects.filter(user=user).order_by('-created_at')
    return render(request, 'dashboard/dashboard.html', {
        'reservations': reservations,
    })

def property_search(request):
    form = PropertySearchForm(request.GET or None)
    properties = Property.objects.all()

    if form.is_valid():
        # Récupérer les données du formulaire
        min_price = form.cleaned_data.get('min_price')
        max_price = form.cleaned_data.get('max_price')
        location = form.cleaned_data.get('location')
        property_type = form.cleaned_data.get('property_type')
        bedrooms = form.cleaned_data.get('bedrooms')
        bathrooms = form.cleaned_data.get('bathrooms')
        min_area = form.cleaned_data.get('min_area')
        max_area = form.cleaned_data.get('max_area')

        # Appliquer les filtres
        if min_price:
            properties = properties.filter(price__gte=min_price)
        if max_price:
            properties = properties.filter(price__lte=max_price)
        if location:
            properties = properties.filter(
                Q(location__icontains=location)
            )
        if property_type:
            properties = properties.filter(property_type=property_type)
        if bedrooms:
            properties = properties.filter(bedrooms=bedrooms)
        if bathrooms:
            properties = properties.filter(bathrooms=bathrooms)
        if min_area:
            properties = properties.filter(area__gte=min_area)
        if max_area:
            properties = properties.filter(area__lte=max_area)

    # Ordonner les résultats par date de création
    properties = properties.order_by('-created_at')

    context = {
        'form': form,
        'properties': properties,
        'count': properties.count(),
    }

    if request.htmx:
        return render(request, 'properties/partials/search_results.html', context)
    return render(request, 'properties/search.html', context)

def property_detail(request, pk):
    property = get_object_or_404(Property, pk=pk)
    similar_properties = Property.objects.filter(
        property_type=property.property_type
    ).exclude(id=property.id)[:3]
    
    context = {
        'property': property,
        'similar_properties': similar_properties,
    }
    return render(request, 'properties/detail.html', context)

@login_required
def contact_seller(request, property_id):
    property = get_object_or_404(Property, id=property_id)
    
    if request.method == 'POST':
        form = PropertyMessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.property = property
            message.sender = request.user
            message.recipient = property.seller
            message.save()
            
            messages.success(request, "Votre message a été envoyé avec succès!")
            return redirect('properties:detail', pk=property_id)
    else:
        form = PropertyMessageForm()

    return render(request, 'properties/contact_form.html', {
        'form': form,
        'property': property
    })

def seller_contacts(request, property_id):
    property = get_object_or_404(Property, id=property_id)
    contact_info = property.get_contact_info()
    
    return render(request, 'properties/seller_contacts.html', {
        'property': property,
        'contact_info': contact_info,
    })