from django.conf import settings
from django.contrib.auth import get_user
from django.utils.deprecation import MiddlewareMixin

class SeparateAdminSessionMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Déterminer si nous sommes dans l'interface d'administration
        is_admin = request.path.startswith('/admin/')
        
        # Définir le nom du cookie de session approprié
        if is_admin:
            settings.SESSION_COOKIE_NAME = settings.ADMIN_SESSION_COOKIE_NAME
        else:
            settings.SESSION_COOKIE_NAME = 'sessionid_site'

    def process_response(self, request, response):
        # Réinitialiser le nom du cookie de session par défaut
        settings.SESSION_COOKIE_NAME = 'sessionid_site'
        return response