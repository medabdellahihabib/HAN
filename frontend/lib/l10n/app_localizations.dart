import 'package:flutter/material.dart';

class AppLocalizations {
  final Locale locale;

  AppLocalizations(this.locale);

  static AppLocalizations of(BuildContext context) {
    return Localizations.of<AppLocalizations>(context, AppLocalizations)!;
  }

  static const LocalizationsDelegate<AppLocalizations> delegate =
      _AppLocalizationsDelegate();

  static final Map<String, Map<String, String>> _localizedValues = {
    'ar': {
      // Authentification
      'app_name': 'حنايه',
      'welcome': 'مرحبا بك',
      'login': 'تسجيل الدخول',
      'register': 'إنشاء حساب',
      'logout': 'تسجيل الخروج',
      'username': 'اسم المستخدم',
      'password': 'كلمة المرور',
      'confirm_password': 'تأكيد كلمة المرور',
      'first_name': 'الاسم الأول',
      'last_name': 'اسم العائلة',
      'phone_number': 'رقم الهاتف',
      'age': 'العمر',
      'gender': 'الجنس',
      'male': 'ذكر',
      'female': 'أنثى',
      
      // Navigation
      'home': 'الرئيسية',
      'profile': 'الملف الشخصي',
      'my_orders': 'طلباتي',
      'settings': 'الإعدادات',
      
      // Henné
      'order_henna': 'طلب حنايه',
      'henna_types': 'أنواع الحناء',
      'order_now': 'اطلب الآن',
      'price': 'السعر',
      'description': 'الوصف',
      
      // Order
      'order_success': 'شكرا على الثقة و سنتواصل معكم قريبا',
      'order_details': 'تفاصيل الطلب',
      'address': 'العنوان',
      'notes': 'ملاحظات',
      'status': 'الحالة',
      'pending': 'قيد الانتظار',
      'confirmed': 'مؤكد',
      'completed': 'مكتمل',
      
      // Language
      'language': 'اللغة',
      'arabic': 'العربية',
      'french': 'Français',
      'change_language': 'تغيير اللغة',
      
      // Buttons
      'submit': 'إرسال',
      'cancel': 'إلغاء',
      'save': 'حفظ',
      'back': 'رجوع',
      
      // Messages
      'loading': 'جاري التحميل...',
      'error': 'حدث خطأ',
      'success': 'نجح العملية',
      'no_data': 'لا توجد بيانات',
    },
    'fr': {
      // Authentification
      'app_name': 'Henné',
      'welcome': 'Bienvenue',
      'login': 'Connexion',
      'register': 'Créer un compte',
      'logout': 'Déconnexion',
      'username': 'Nom d\'utilisateur',
      'password': 'Mot de passe',
      'confirm_password': 'Confirmer le mot de passe',
      'first_name': 'Prénom',
      'last_name': 'Nom',
      'phone_number': 'Numéro de téléphone',
      'age': 'Âge',
      'gender': 'Genre',
      'male': 'Homme',
      'female': 'Femme',
      
      // Navigation
      'home': 'Accueil',
      'profile': 'Profil',
      'my_orders': 'Mes commandes',
      'settings': 'Paramètres',
      
      // Henné
      'order_henna': 'Commander du henné',
      'henna_types': 'Types de henné',
      'order_now': 'Commander maintenant',
      'price': 'Prix',
      'description': 'Description',
      
      // Order
      'order_success': 'Merci pour votre confiance, nous vous contactons bientôt',
      'order_details': 'Détails de la commande',
      'address': 'Adresse',
      'notes': 'Notes',
      'status': 'Statut',
      'pending': 'En attente',
      'confirmed': 'Confirmé',
      'completed': 'Terminé',
      
      // Language
      'language': 'Langue',
      'arabic': 'العربية',
      'french': 'Français',
      'change_language': 'Changer la langue',
      
      // Buttons
      'submit': 'Envoyer',
      'cancel': 'Annuler',
      'save': 'Enregistrer',
      'back': 'Retour',
      
      // Messages
      'loading': 'Chargement...',
      'error': 'Une erreur s\'est produite',
      'success': 'Opération réussie',
      'no_data': 'Aucune donnée',
    },
  };

  String translate(String key) {
    return _localizedValues[locale.languageCode]?[key] ?? key;
  }
}

class _AppLocalizationsDelegate
    extends LocalizationsDelegate<AppLocalizations> {
  const _AppLocalizationsDelegate();

  @override
  bool isSupported(Locale locale) {
    return ['ar', 'fr'].contains(locale.languageCode);
  }

  @override
  Future<AppLocalizations> load(Locale locale) async {
    return AppLocalizations(locale);
  }

  @override
  bool shouldReload(_AppLocalizationsDelegate old) => false;
}