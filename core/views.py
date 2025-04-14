from django.shortcuts import render, redirect
from properties.models import Property
from django.core.mail import send_mail
from django.contrib import messages

def home(request):
    featured_properties = Property.objects.all().order_by('-created_at')[:4]
    latest_properties = Property.objects.all().order_by('-created_at')[:6]
    
    context = {
        'featured_properties': featured_properties,
        'latest_properties': latest_properties,
    }
    return render(request, 'core/home.html', context)

def about(request):
    context = {
        'title': 'À propos de nous',
        'description': 'ImmoBénin est votre partenaire de confiance pour trouver le bien immobilier idéal au Bénin.',
    }
    return render(request, 'core/about.html', context)

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        
        # Envoi d'email (à configurer dans settings.py)
        try:
            send_mail(
                f'Contact de {name}',
                message,
                email,
                ['contact@immobenin.com'],
                fail_silently=False,
            )
            messages.success(request, 'Votre message a été envoyé avec succès!')
            return redirect('core:contact')
        except:
            messages.error(request, 'Une erreur est survenue. Veuillez réessayer.')
    
    return render(request, 'core/contact.html')
