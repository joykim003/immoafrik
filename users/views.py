from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from .forms import SignUpForm, LoginForm, UserEditForm
from properties.models import Property  # Ajout de l'import

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                login(request, user)
                messages.success(request, 'Inscription réussie!')
                return redirect('core:home')
            except Exception as e:
                messages.error(request, str(e))
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = SignUpForm()
    
    return render(request, 'users/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            # Créer une nouvelle session pour le site
            request.session.create()
            login(request, user)
            messages.success(request, f'Bienvenue {user.username}!')
            return redirect('core:home')
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})

@login_required
def profile(request):
    return render(request, 'users/profile.html', {
        'user': request.user
    })

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profil mis à jour avec succès!')
            return redirect('users:profile')
    else:
        form = UserEditForm(instance=request.user)
    
    return render(request, 'users/edit_profile.html', {'form': form})

@require_http_methods(["POST"])
def logout_view(request):
    # Ne déconnecter que la session du site
    if 'sessionid_site' in request.COOKIES:
        logout(request)
        messages.success(request, 'Vous avez été déconnecté avec succès.')
    return redirect('core:home')

@login_required
def dashboard_view(request):
    context = {
        'visited_properties_count': 0,  # À implémenter
        'favorites_count': 0,  # À implémenter
        'messages_count': 0,  # À implémenter
        'recent_activities': [],  # À implémenter
        'favorite_properties': [],  # À implémenter
        'user_properties': Property.objects.filter(seller=request.user).order_by('-created_at'),
    }
    return render(request, 'users/dashboard.html', context)
