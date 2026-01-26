from rest_framework import serializers
from .models import CustomUser, HennaType, Order

# ----------------------------
# Serializer pour l'inscription
# ----------------------------
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    
    class Meta:
        model = CustomUser
        fields = [
            'username', 'password', 'first_name', 'last_name',
            'phone_number', 'gender', 'age', 'language_preference'
        ]
    
    def create(self, validated_data):
        # Utiliser create_user du manager personnalisé
        password = validated_data.pop('password')
        user = CustomUser.objects.create_user(
            password=password,
            **validated_data
        )
        return user


# ----------------------------
# Serializer pour le profil utilisateur
# ----------------------------
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'id', 'username', 'first_name', 'last_name',
          'phone_number', 'gender', 'age',
            'language_preference', 'created_at'
        ]
        read_only_fields = ['id', 'username', 'created_at']


# ----------------------------
# Serializer pour les types de henné
# ----------------------------
class HennaTypeSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = HennaType
        fields = [
            'id', 'name', 'description', 'image_url',
            'price', 'is_available'
        ]
    
    def get_name(self, obj):
        request = self.context.get('request')
        if request and hasattr(request.user, 'language_preference'):
            lang = request.user.language_preference
            if lang == 'fr' and obj.name_fr:
                return obj.name_fr
        return obj.name_ar
    
    def get_description(self, obj):
        request = self.context.get('request')
        if request and hasattr(request.user, 'language_preference'):
            lang = request.user.language_preference
            if lang == 'fr' and obj.description_fr:
                return obj.description_fr
        return obj.description_ar
    
    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image:
            return request.build_absolute_uri(obj.image.url)
        return None


# ----------------------------
# Serializer pour les commandes
# ----------------------------
class OrderSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source='client.first_name', read_only=True)
    client_phone = serializers.CharField(source='client.phone_number', read_only=True)
    henna_name = serializers.CharField(source='henna_type.name_ar', read_only=True)
    henna_price = serializers.DecimalField(
        source='henna_type.price',
        max_digits=10,
        decimal_places=2,
        read_only=True
    )
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Order
        fields = [
            'id', 'client', 'client_name', 'client_phone',
            'henna_type', 'henna_name', 'henna_price',
            'status', 'status_display', 'notes', 'address',
            'appointment_date', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'client', 'created_at', 'updated_at']


# ----------------------------
# Serializer pour créer une commande
# ----------------------------
class CreateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['henna_type', 'notes', 'address', 'appointment_date']
    
    def create(self, validated_data):
        validated_data['client'] = self.context['request'].user
        return super().create(validated_data)