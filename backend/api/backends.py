from django.contrib.auth.backends import ModelBackend
from .models import CustomUser

class PhoneBackend(ModelBackend):
    """
    Backend d'authentification personnalisé qui permet de se connecter
    avec username OU phone_number
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Essayer d'abord avec username
            user = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            try:
                # Essayer avec phone_number
                user = CustomUser.objects.get(phone_number=username)
            except CustomUser.DoesNotExist:
                return None
        
        # Vérifier le mot de passe
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        
        return None