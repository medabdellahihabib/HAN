from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, HennaType, Order

# ----------------------------
# Admin User personnalisé
# ----------------------------
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'first_name', 'last_name', 'phone_number', 'gender', 'age', 'is_staff']
    list_filter = ['gender', 'language_preference', 'is_staff']
    search_fields = ['username', 'first_name', 'last_name', 'phone_number']
    
    fieldsets = UserAdmin.fieldsets + (
        ('معلومات إضافية', {'fields': ('phone_number', 'gender', 'age', 'language_preference')}),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('معلومات إضافية', {'fields': ('phone_number', 'gender', 'age', 'language_preference')}),
    )


# ----------------------------
# Admin Type de Henné
# ----------------------------
@admin.register(HennaType)
class HennaTypeAdmin(admin.ModelAdmin):
    list_display = ['name_ar', 'name_fr', 'price', 'is_available', 'created_at']
    list_filter = ['is_available', 'created_at']
    search_fields = ['name_ar', 'name_fr']
    list_editable = ['is_available', 'price']


# ----------------------------
# Admin Commandes
# ----------------------------
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'client', 'henna_type', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['client__first_name', 'client__last_name', 'client__phone_number']
    list_editable = ['status']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('معلومات الطلب', {
            'fields': ('client', 'henna_type', 'status')
        }),
        ('التفاصيل', {
            'fields': ('notes', 'address', 'appointment_date')
        }),
        ('التواريخ', {
            'fields': ('created_at', 'updated_at')
        }),
    )