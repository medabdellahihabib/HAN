from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import RegexValidator

# ----------------------------
# Manager personnalisé pour CustomUser
# ----------------------------
class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, username, password=None, **extra_fields):
        """
        Crée et sauvegarde un utilisateur.
        """
        if not username:
            raise ValueError("Le nom d'utilisateur doit être renseigné")
        
        # S'assurer que phone_number est présent
        phone_number = extra_fields.get('phone_number')
        if not phone_number:
            raise ValueError("Le numéro de téléphone doit être renseigné")
        

        
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        """
        Crée et sauvegarde un superutilisateur.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        # Valeurs par défaut pour les champs requis
        extra_fields.setdefault('phone_number', '+22200000000')
        extra_fields.setdefault('gender', 'M')
        extra_fields.setdefault('age', 30)
        extra_fields.setdefault('first_name', 'Admin')
        extra_fields.setdefault('last_name', 'User')


        if extra_fields.get('is_staff') is not True:
            raise ValueError('Le superuser doit avoir is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Le superuser doit avoir is_superuser=True.')

        return self.create_user(username, password, **extra_fields)

# ----------------------------
# Modèle CustomUser
# ----------------------------
class CustomUser(AbstractUser):
    # ----------------------------
    # Identifiant principal = phone_number
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    # ----------------------------
    GENDER_CHOICES = [
        ('M', 'ذكر'),
        ('F', 'أنثى'),
    ]
    
    LANGUAGE_CHOICES = [
        ('ar', 'العربية'),
        ('fr', 'Français'),
    ]

    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="رقم الهاتف يجب أن يكون بالصيغة: '+999999999'. يسمح بـ 15 رقمًا كحد أقصى."
    )
    
    phone_number = models.CharField(
        validators=[phone_regex],
        max_length=17,
        unique=True,
        verbose_name="رقم الهاتف"
    )
    
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        verbose_name="الجنس"
    )
    
    age = models.PositiveIntegerField(
        verbose_name="العمر"
    )
    
    language_preference = models.CharField(
        max_length=2,
        choices=LANGUAGE_CHOICES,
        default='ar',
        verbose_name="اللغة المفضلة"
    )
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ التسجيل")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاريخ التحديث")

    # ⚠️ Corrige les conflits avec AbstractUser
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='المجموعات',
        blank=True,
        related_name='customuser_set',
        related_query_name='customuser',
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='صلاحيات المستخدم',
        blank=True,
        related_name='customuser_set',
        related_query_name='customuser',
    )

    # ----------------------------
    objects = CustomUserManager()  # Manager personnalisé
    
    class Meta:
        verbose_name = "مستخدم"
        verbose_name_plural = "المستخدمون"

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.phone_number})"



# ----------------------------
# Modèle Type de Henné
# ----------------------------
class HennaType(models.Model):
    name_ar = models.CharField(max_length=100, verbose_name="الاسم بالعربية")
    name_fr = models.CharField(max_length=100, blank=True, verbose_name="الاسم بالفرنسية")
    
    description_ar = models.TextField(verbose_name="الوصف بالعربية")
    description_fr = models.TextField(blank=True, verbose_name="الوصف بالفرنسية")
    
    image = models.ImageField(upload_to='henna_types/', verbose_name="صورة")
    
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="السعر"
    )
    
    is_available = models.BooleanField(default=True, verbose_name="متاح")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاريخ التحديث")
    
    class Meta:
        verbose_name = "نوع الحناء"
        verbose_name_plural = "أنواع الحناء"
        ordering = ['name_ar']
    
    def __str__(self):
        return self.name_ar

# ----------------------------
# Modèle Commande
# ----------------------------
class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'قيد الانتظار'),      # En attente
        ('confirmed', 'مؤكد'),            # Confirmé
        ('in_progress', 'قيد التنفيذ'),   # En cours
        ('completed', 'مكتمل'),           # Terminé
        ('cancelled', 'ملغي'),            # Annulé
    ]
    
    client = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name="العميل"
    )
    
    henna_type = models.ForeignKey(
        HennaType,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name="نوع الحناء"
    )
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name="الحالة"
    )
    
    notes = models.TextField(
        blank=True,
        verbose_name="ملاحظات"
    )
    
    address = models.TextField(
        verbose_name="العنوان",
        blank=True
    )
    
    appointment_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="تاريخ الموعد"
    )
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الطلب")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاريخ التحديث")
    
    class Meta:
        verbose_name = "طلب"
        verbose_name_plural = "الطلبات"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"طلب #{self.id} - {self.client.first_name} - {self.henna_type.name_ar}"