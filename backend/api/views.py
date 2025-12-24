from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# ----------------------------
# API simple de test
# ----------------------------
@api_view(['GET'])
@permission_classes([AllowAny])
def hello_api(request):
    return Response({
        "message": "Hello from Django backend 🚀"
    })

# ----------------------------
# API Register (Création de compte)
# ----------------------------
@api_view(['POST'])
@permission_classes([AllowAny])
def register_api(request):
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email', '')  # Optionnel
    first_name = request.data.get('first_name', '')  # Optionnel
    last_name = request.data.get('last_name', '')  # Optionnel

    # Validation des données
    if not username or not password:
        return Response(
            {"error": "Le nom d'utilisateur et le mot de passe sont requis"}, 
            status=status.HTTP_400_BAD_REQUEST
        )

    # Vérifier si l'utilisateur existe déjà
    if User.objects.filter(username=username).exists():
        return Response(
            {"error": "Ce nom d'utilisateur est déjà pris"}, 
            status=status.HTTP_400_BAD_REQUEST
        )

    # Vérifier l'email si fourni
    if email and User.objects.filter(email=email).exists():
        return Response(
            {"error": "Cet email est déjà utilisé"}, 
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        # Créer l'utilisateur
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email if email else '',
            first_name=first_name,
            last_name=last_name
        )
        
        # Connecter automatiquement l'utilisateur après inscription
        login(request, user)
        
        return Response({
            "message": "Compte créé avec succès",
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "date_joined": user.date_joined
        }, status=status.HTTP_201_CREATED)
        
    except ValidationError as e:
        return Response(
            {"error": str(e)}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        return Response(
            {"error": "Une erreur est survenue lors de la création du compte"}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

# ----------------------------
# API Login
# ----------------------------
@api_view(['POST'])
@permission_classes([AllowAny])
def login_api(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response(
            {"error": "Le nom d'utilisateur et le mot de passe sont requis"}, 
            status=status.HTTP_400_BAD_REQUEST
        )

    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        return Response({
            "message": "Login successful",
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name
        })
    else:
        return Response(
            {"error": "Identifiant ou mot de passe incorrect"}, 
            status=status.HTTP_400_BAD_REQUEST
        )

# ----------------------------
# API Logout
# ----------------------------
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_api(request):
    logout(request)
    return Response({"message": "Logout successful"})

# ----------------------------
# API Profil utilisateur
# ----------------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile_api(request):
    user = request.user
    return Response({
        "username": user.username,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "date_joined": user.date_joined,
        "last_login": user.last_login
    })

# ----------------------------
# API Mise à jour du profil
# ----------------------------
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_profile_api(request):
    user = request.user
    
    email = request.data.get('email')
    first_name = request.data.get('first_name')
    last_name = request.data.get('last_name')
    
    if email:
        # Vérifier si l'email n'est pas déjà utilisé par un autre utilisateur
        if User.objects.filter(email=email).exclude(id=user.id).exists():
            return Response(
                {"error": "Cet email est déjà utilisé par un autre compte"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        user.email = email
    
    if first_name is not None:
        user.first_name = first_name
    
    if last_name is not None:
        user.last_name = last_name
    
    try:
        user.save()
        return Response({
            "message": "Profil mis à jour avec succès",
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name
        })
    except Exception as e:
        return Response(
            {"error": "Erreur lors de la mise à jour du profil"}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

# ----------------------------
# API Changer le mot de passe
# ----------------------------
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password_api(request):
    user = request.user
    
    old_password = request.data.get('old_password')
    new_password = request.data.get('new_password')
    
    if not old_password or not new_password:
        return Response(
            {"error": "L'ancien et le nouveau mot de passe sont requis"}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Vérifier l'ancien mot de passe
    if not user.check_password(old_password):
        return Response(
            {"error": "L'ancien mot de passe est incorrect"}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        user.set_password(new_password)
        user.save()
        
        # Reconnecter l'utilisateur avec le nouveau mot de passe
        login(request, user)
        
        return Response({"message": "Mot de passe changé avec succès"})
    except Exception as e:
        return Response(
            {"error": "Erreur lors du changement de mot de passe"}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

# ----------------------------
# Exemple API protégée (home)
# ----------------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def home_api(request):
    return Response({"message": f"Bienvenue {request.user.username} sur Flutter backend"})