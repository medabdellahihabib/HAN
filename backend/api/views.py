from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from django.contrib.auth import authenticate
from .models import CustomUser, HennaType, Order
from .serializers import (
    RegisterSerializer, UserSerializer,
    HennaTypeSerializer, OrderSerializer, CreateOrderSerializer
)

# Import Token avec un nom différent pour éviter les conflits
from rest_framework.authtoken.models import Token as AuthToken

# ----------------------------
# Configuration des messages selon la langue
# ----------------------------
MESSAGES = {
    'ar': {
        'register_success': 'تم إنشاء الحساب بنجاح',
        'login_success': 'تم تسجيل الدخول بنجاح',
        'logout_success': 'تم تسجيل الخروج بنجاح',
        'order_success': 'شكرا على الثقة و سنتواصل معكم قريبا',
        'profile_updated': 'تم تحديث الملف الشخصي بنجاح',
        'password_changed': 'تم تغيير كلمة المرور بنجاح',
        'invalid_credentials': 'اسم المستخدم أو كلمة المرور غير صحيحة',
        'missing_fields': 'يرجى ملء جميع الحقول المطلوبة',
    },
    'fr': {
        'register_success': 'Compte créé avec succès',
        'login_success': 'Connexion réussie',
        'logout_success': 'Déconnexion réussie',
        'order_success': 'Merci pour votre confiance, nous vous contactons bientôt',
        'profile_updated': 'Profil mis à jour avec succès',
        'password_changed': 'Mot de passe changé avec succès',
        'invalid_credentials': 'Nom d\'utilisateur ou mot de passe incorrect',
        'missing_fields': 'Veuillez remplir tous les champs requis',
    }
}

def get_message(lang, key):
    """Récupère le message selon la langue"""
    return MESSAGES.get(lang, MESSAGES['ar']).get(key)


# ----------------------------
# API Test
# ----------------------------
@api_view(['GET'])
@permission_classes([AllowAny])
def hello_api(request):
    return Response({
        "message": "مرحبا بك في تطبيق الحناء 🎨",
        "message_fr": "Bienvenue dans l'application Henné 🎨"
    })


# ----------------------------
# API Inscription (Register)
# ----------------------------
@api_view(['POST'])
@permission_classes([AllowAny])
def register_api(request):
    """API d'inscription"""
    print("=== REGISTER REQUEST ===")
    print("Data received:", request.data)
    
    serializer = RegisterSerializer(data=request.data)
    
    if serializer.is_valid():
        try:
            user = serializer.save()
            
            # Créer le token pour l'utilisateur
            token = AuthToken.objects.create(user=user)
            
            lang = user.language_preference
            
            print(f"✅ User created successfully: {user.username}")
            
            return Response({
                "message": get_message(lang, 'register_success'),
                "token": token.key,
                "user": UserSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            print(f"❌ Error creating user: {str(e)}")
            import traceback
            traceback.print_exc()
            
            return Response({
                "error": f"Error creating user: {str(e)}"
            }, status=status.HTTP_400_BAD_REQUEST)
    
    print("❌ Validation errors:", serializer.errors)
    return Response({
        "error": "Validation failed",
        "details": serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


# ----------------------------
# API Connexion (Login)
# ----------------------------
@api_view(['POST'])
@permission_classes([AllowAny])
def login_api(request):
    """API de connexion - accepte username OU phone_number"""
    identifier = request.data.get('username')  # Peut être username ou phone
    password = request.data.get('password')
    
    print("=== LOGIN REQUEST ===")
    print(f"Identifier: {identifier}")
    
    if not identifier or not password:
        return Response(
            {"error": "يرجى إدخال اسم المستخدم وكلمة المرور"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Authentifier avec le backend personnalisé (PhoneBackend)
    user = authenticate(request, username=identifier, password=password)
    
    if user is not None:
        # Créer ou récupérer le token
        token, created = AuthToken.objects.get_or_create(user=user)
        lang = user.language_preference
        
        print(f"✅ Login successful for: {user.username}")
        
        return Response({
            "message": get_message(lang, 'login_success'),
            "token": token.key,
            "user": UserSerializer(user).data
        })
    
    print("❌ Authentication failed")
    return Response(
        {"error": "اسم المستخدم أو كلمة المرور غير صحيحة"},
        status=status.HTTP_400_BAD_REQUEST
    )


# ----------------------------
# API Déconnexion (Logout)
# ----------------------------
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_api(request):
    """Déconnexion - Supprimer le token"""
    try:
        # Supprimer le token de l'utilisateur
        AuthToken.objects.filter(user=request.user).delete()
    except Exception as e:
        print(f"Error during logout: {e}")
    
    lang = request.user.language_preference
    return Response({"message": get_message(lang, 'logout_success')})
# ----------------------------
# API Profil utilisateur
# ----------------------------
@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def profile_api(request):
    user = request.user
    
    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            lang = user.language_preference
            return Response({
                "message": get_message(lang, 'profile_updated'),
                "user": serializer.data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
            {"error": "يرجى إدخال كلمة المرور القديمة والجديدة"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if not user.check_password(old_password):
        return Response(
            {"error": "كلمة المرور القديمة غير صحيحة"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    user.set_password(new_password)
    user.save()
    
    # Régénérer le token après changement de mot de passe
    AuthToken.objects.filter(user=user).delete()
    token = AuthToken.objects.create(user=user)
    
    lang = user.language_preference
    return Response({
        "message": get_message(lang, 'password_changed'),
        "token": token.key  # Nouveau token
    })


# ----------------------------
# API Changer la langue
# ----------------------------
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_language_api(request):
    user = request.user
    language = request.data.get('language')
    
    if language not in ['ar', 'fr']:
        return Response(
            {"error": "اللغة غير صالحة / Langue invalide"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    user.language_preference = language
    user.save()
    
    return Response({
        "message": "تم تغيير اللغة بنجاح" if language == 'ar' else "Langue changée avec succès",
        "language": language
    })


# ========================================
# APIs pour les types de henné
# ========================================

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def henna_types_list_api(request):
    """Liste tous les types de henné disponibles"""
    henna_types = HennaType.objects.filter(is_available=True)
    serializer = HennaTypeSerializer(
        henna_types,
        many=True,
        context={'request': request}
    )
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def henna_type_detail_api(request, pk):
    """Détails d'un type de henné"""
    try:
        henna_type = HennaType.objects.get(pk=pk, is_available=True)
        serializer = HennaTypeSerializer(henna_type, context={'request': request})
        return Response(serializer.data)
    except HennaType.DoesNotExist:
        return Response(
            {"error": "نوع الحناء غير موجود"},
            status=status.HTTP_404_NOT_FOUND
        )


# ========================================
# APIs pour les commandes
# ========================================

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_order_api(request):
    """Créer une nouvelle commande - طلب حناء"""
    serializer = CreateOrderSerializer(
        data=request.data,
        context={'request': request}
    )
    
    if serializer.is_valid():
        order = serializer.save()
        lang = request.user.language_preference
        
        return Response({
            "message": get_message(lang, 'order_success'),
            "order": OrderSerializer(order).data
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_orders_api(request):
    """Liste des commandes de l'utilisateur connecté"""
    orders = Order.objects.filter(client=request.user)
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def order_detail_api(request, pk):
    """Détails d'une commande"""
    try:
        order = Order.objects.get(pk=pk, client=request.user)
        serializer = OrderSerializer(order)
        return Response(serializer.data)
    except Order.DoesNotExist:
        return Response(
            {"error": "الطلب غير موجود"},
            status=status.HTTP_404_NOT_FOUND
        )


# ========================================
# APIs ADMIN - Dashboard
# ========================================

@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_dashboard_api(request):
    """Dashboard admin - statistiques générales"""
    total_orders = Order.objects.count()
    pending_orders = Order.objects.filter(status='pending').count()
    completed_orders = Order.objects.filter(status='completed').count()
    total_clients = CustomUser.objects.filter(is_staff=False).count()
    
    return Response({
        "total_orders": total_orders,
        "pending_orders": pending_orders,
        "completed_orders": completed_orders,
        "total_clients": total_clients
    })


@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_orders_list_api(request):
    """Liste de toutes les commandes pour l'admin"""
    status_filter = request.GET.get('status')
    
    orders = Order.objects.all()
    if status_filter:
        orders = orders.filter(status=status_filter)
    
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)


@api_view(['GET', 'PUT'])
@permission_classes([IsAdminUser])
def admin_order_detail_api(request, pk):
    """Détails et modification d'une commande par l'admin"""
    try:
        order = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        return Response(
            {"error": "الطلب غير موجود"},
            status=status.HTTP_404_NOT_FOUND
        )
    
    if request.method == 'GET':
        serializer = OrderSerializer(order)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = OrderSerializer(order, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "تم تحديث الطلب بنجاح",
                "order": serializer.data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_clients_list_api(request):
    """Liste de tous les clients"""
    clients = CustomUser.objects.filter(is_staff=False)
    serializer = UserSerializer(clients, many=True)
    return Response(serializer.data)
# Le reste de votre code reste identique...
# ----------------------------
# API Profil utilisateur
# ----------------------------
@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def profile_api(request):
    user = request.user
    
    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            lang = user.language_preference
            return Response({
                "message": get_message(lang, 'profile_updated'),
                "user": serializer.data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
            {"error": "يرجى إدخال كلمة المرور القديمة والجديدة"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if not user.check_password(old_password):
        return Response(
            {"error": "كلمة المرور القديمة غير صحيحة"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    user.set_password(new_password)
    user.save()
    login(request, user)
    
    lang = user.language_preference
    return Response({"message": get_message(lang, 'password_changed')})


# ----------------------------
# API Changer la langue
# ----------------------------
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_language_api(request):
    user = request.user
    language = request.data.get('language')
    
    if language not in ['ar', 'fr']:
        return Response(
            {"error": "اللغة غير صالحة / Langue invalide"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    user.language_preference = language
    user.save()
    
    return Response({
        "message": "تم تغيير اللغة بنجاح" if language == 'ar' else "Langue changée avec succès",
        "language": language
    })


# ========================================
# APIs pour les types de henné
# ========================================

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def henna_types_list_api(request):
    """Liste tous les types de henné disponibles"""
    henna_types = HennaType.objects.filter(is_available=True)
    serializer = HennaTypeSerializer(
        henna_types,
        many=True,
        context={'request': request}
    )
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def henna_type_detail_api(request, pk):
    """Détails d'un type de henné"""
    try:
        henna_type = HennaType.objects.get(pk=pk, is_available=True)
        serializer = HennaTypeSerializer(henna_type, context={'request': request})
        return Response(serializer.data)
    except HennaType.DoesNotExist:
        return Response(
            {"error": "نوع الحناء غير موجود"},
            status=status.HTTP_404_NOT_FOUND
        )


# ========================================
# APIs pour les commandes
# ========================================

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_order_api(request):
    """Créer une nouvelle commande - طلب حناء"""
    serializer = CreateOrderSerializer(
        data=request.data,
        context={'request': request}
    )
    
    if serializer.is_valid():
        order = serializer.save()
        lang = request.user.language_preference
        
        return Response({
            "message": get_message(lang, 'order_success'),
            "order": OrderSerializer(order).data
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_orders_api(request):
    """Liste des commandes de l'utilisateur connecté"""
    orders = Order.objects.filter(client=request.user)
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def order_detail_api(request, pk):
    """Détails d'une commande"""
    try:
        order = Order.objects.get(pk=pk, client=request.user)
        serializer = OrderSerializer(order)
        return Response(serializer.data)
    except Order.DoesNotExist:
        return Response(
            {"error": "الطلب غير موجود"},
            status=status.HTTP_404_NOT_FOUND
        )


# ========================================
# APIs ADMIN - Dashboard
# ========================================

@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_dashboard_api(request):
    """Dashboard admin - statistiques générales"""
    total_orders = Order.objects.count()
    pending_orders = Order.objects.filter(status='pending').count()
    completed_orders = Order.objects.filter(status='completed').count()
    total_clients = CustomUser.objects.filter(is_staff=False).count()
    
    return Response({
        "total_orders": total_orders,
        "pending_orders": pending_orders,
        "completed_orders": completed_orders,
        "total_clients": total_clients
    })


@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_orders_list_api(request):
    """Liste de toutes les commandes pour l'admin"""
    status_filter = request.GET.get('status')
    
    orders = Order.objects.all()
    if status_filter:
        orders = orders.filter(status=status_filter)
    
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)


@api_view(['GET', 'PUT'])
@permission_classes([IsAdminUser])
def admin_order_detail_api(request, pk):
    """Détails et modification d'une commande par l'admin"""
    try:
        order = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        return Response(
            {"error": "الطلب غير موجود"},
            status=status.HTTP_404_NOT_FOUND
        )
    
    if request.method == 'GET':
        serializer = OrderSerializer(order)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = OrderSerializer(order, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "تم تحديث الطلب بنجاح",
                "order": serializer.data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_clients_list_api(request):
    """Liste de tous les clients"""
    clients = CustomUser.objects.filter(is_staff=False)
    serializer = UserSerializer(clients, many=True)
    return Response(serializer.data)




@api_view(['POST'])
@permission_classes([AllowAny])
def register_api(request):
    """API d'inscription"""
    print("=== REGISTER REQUEST ===")
    print("Data received:", request.data)
    
    # Vérifier les champs requis
    required_fields = ['username', 'password', 'first_name', 'last_name', 'phone_number', 'gender', 'age']
    
    missing_fields = [field for field in required_fields if not request.data.get(field)]
    
    if missing_fields:
        return Response({
            "error": f"Missing required fields: {', '.join(missing_fields)}",
            "details": {field: ["This field is required."] for field in missing_fields}
        }, status=status.HTTP_400_BAD_REQUEST)
    
    serializer = RegisterSerializer(data=request.data)
    
    if serializer.is_valid():
        try:
            user = serializer.save()
            
            # Créer le token pour l'utilisateur
            token, created = AuthToken.objects.get_or_create(user=user)
            
            lang = user.language_preference
            
            print(f"✅ User created successfully: {user.username}")
            
            return Response({
                "message": get_message(lang, 'register_success'),
                "token": token.key,
                "user": UserSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            print(f"❌ Error creating user: {str(e)}")
            import traceback
            traceback.print_exc()
            
            return Response({
                "error": f"Error creating user: {str(e)}"
            }, status=status.HTTP_400_BAD_REQUEST)
    
    print("❌ Validation errors:", serializer.errors)
    return Response({
        "error": "Validation failed",
        "details": serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)    