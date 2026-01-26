class AppConstants {
  // API Configuration
  static const String baseUrl = 'http://localhost:3000'; // Base URL sans /api
  static const String registerEndpoint = '/register/';
  static const String loginEndpoint = '/login/';  
  // SharedPreferences Keys
  static const String userKey = 'user';
  static const String tokenKey = 'token';
  static const String isLoggedInKey = 'isLoggedIn';
  static const String languageKey = 'language';
  static const String themeKey = 'theme';
  
  // Default Values
  static const String defaultLanguage = 'ar';
  static const String defaultTheme = 'light';
  
  // API Endpoints - Endpoints complets utilisés par votre API service existant
  static const String loginEndpoint = '/auth/login';
  static const String registerEndpoint = '/auth/register';
  static const String logoutEndpoint = '/auth/logout';
  static const String userEndpoint = '/user';
  static const String ordersEndpoint = '/orders';
  static const String productsEndpoint = '/products';
  
  // Endpoints supplémentaires pour l'API Henna
  static const String hennaTypesEndpoint = '/henna/types';
  static const String createOrderEndpoint = '/orders/create';
  static const String myOrdersEndpoint = '/orders/my-orders';
  static const String changeLanguageEndpoint = '/user/change-language';
  
  // Timeout Duration
  static const Duration connectionTimeout = Duration(seconds: 30);
  static const Duration receiveTimeout = Duration(seconds: 30);
  
  // Pagination
  static const int pageSize = 20;
  static const int initialPage = 1;
  
  // Image Configuration
  static const int maxImageSize = 5 * 1024 * 1024; // 5 MB
  static const List<String> allowedImageTypes = ['jpg', 'jpeg', 'png', 'gif'];
  
  // Validation
  static const int minPasswordLength = 6;
  static const int maxPasswordLength = 50;
  static const int minUsernameLength = 3;
  static const int maxUsernameLength = 30;
  
  // App Information
  static const String appName = 'HAN';
  static const String appVersion = '1.0.0';
  
  // Error Messages (Arabic)
  static const String networkError = 'خطأ في الشبكة. يرجى التحقق من الاتصال.';
  static const String serverError = 'خطأ في الخادم. يرجى المحاولة لاحقاً.';
  static const String unknownError = 'حدث خطأ غير معروف.';
  static const String authError = 'فشل المصادقة. يرجى تسجيل الدخول مرة أخرى.';
  
  // Success Messages (Arabic)
  static const String loginSuccess = 'تم تسجيل الدخول بنجاح';
  static const String registerSuccess = 'تم التسجيل بنجاح';
  static const String logoutSuccess = 'تم تسجيل الخروج بنجاح';
  static const String updateSuccess = 'تم التحديث بنجاح';
  
  // Regular Expressions
  static final RegExp emailRegex = RegExp(
    r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
  );
  static final RegExp phoneRegex = RegExp(
    r'^[+]?[(]?[0-9]{1,4}[)]?[-\s\.]?[(]?[0-9]{1,4}[)]?[-\s\.]?[0-9]{1,9}$',
  );
  
  // Cache Duration
  static const Duration cacheExpiry = Duration(hours: 24);
  
  // Debounce Duration (for search)
  static const Duration debounceDuration = Duration(milliseconds: 500);
  
  // Animation Duration
  static const Duration shortAnimationDuration = Duration(milliseconds: 200);
  static const Duration mediumAnimationDuration = Duration(milliseconds: 300);
  static const Duration longAnimationDuration = Duration(milliseconds: 500);
  
  // Private constructor to prevent instantiation
  AppConstants._();
}