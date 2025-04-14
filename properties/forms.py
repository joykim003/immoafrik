from django import forms
from .models import Property, PropertyMessage  # Ajout de PropertyMessage
from .models import Reservation

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['title', 'description', 'property_type', 'price', 'location', 'image']
        labels = {
            'title': 'Titre',
            'description': 'Description',
            'property_type': 'Type de bien',
            'price': 'Prix (FCFA)',
            'location': 'Localisation',
            'image': 'Image'
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'price': forms.NumberInput(attrs={'min': '0', 'step': '1000'}),
        }

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['property', 'start_date', 'end_date', 'message']

class PropertySearchForm(forms.Form):
    min_price = forms.DecimalField(
        required=False,
        label="Prix minimum",
        widget=forms.NumberInput(attrs={
            'class': 'w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400',
            'placeholder': 'Prix minimum'
        })
    )
    max_price = forms.DecimalField(
        required=False,
        label="Prix maximum",
        widget=forms.NumberInput(attrs={
            'class': 'w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400',
            'placeholder': 'Prix maximum'
        })
    )
    location = forms.CharField(
        required=False,
        label="Localisation",
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400',
            'placeholder': 'Ville, quartier...'
        })
    )
    property_type = forms.ChoiceField(
        required=False,
        label="Type de bien",
        choices=[('', 'Tous types')] + Property.PROPERTY_TYPES,
        widget=forms.Select(attrs={
            'class': 'w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400'
        })
    )
    bedrooms = forms.IntegerField(
        required=False,
        label="Nombre de chambres",
        widget=forms.NumberInput(attrs={
            'class': 'w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400',
            'placeholder': 'Nombre de chambres'
        })
    )
    bathrooms = forms.IntegerField(
        required=False,
        label="Nombre de salles de bain",
        widget=forms.NumberInput(attrs={
            'class': 'w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400',
            'placeholder': 'Nombre de salles de bain'
        })
    )
    min_area = forms.DecimalField(
        required=False,
        label="Surface minimum (m²)",
        widget=forms.NumberInput(attrs={
            'class': 'w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400',
            'placeholder': 'Surface minimum'
        })
    )
    max_area = forms.DecimalField(
        required=False,
        label="Surface maximum (m²)",
        widget=forms.NumberInput(attrs={
            'class': 'w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400',
            'placeholder': 'Surface maximum'
        })
    )

class PropertyMessageForm(forms.ModelForm):
    class Meta:
        model = PropertyMessage
        fields = ['subject', 'message']
        labels = {
            'subject': 'Sujet',
            'message': 'Message'
        }
        widgets = {
            'subject': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg'
            }),
            'message': forms.Textarea(attrs={
                'rows': 4,
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg'
            })
        }
