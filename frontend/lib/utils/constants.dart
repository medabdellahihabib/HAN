class AppConstants {
  // URL de votre backend Django
  static const String baseUrl = 'http://127.0.0.1:8000/api';
  
  // Endpoints
  static const String registerEndpoint = '/register/';
  static const String loginEndpoint = '/login/';
  static const String logoutEndpoint = '/logout/';
  static const String profileEndpoint = '/profile/';
  static const String changeLanguageEndpoint = '/profile/change-language/';
  static const String hennaTypesEndpoint = '/henna-types/';
  static const String createOrderEndpoint = '/orders/create/';
  static const String myOrdersEndpoint = '/orders/my-orders/';
  
  // Clés de stockage
  static const String languageKey = 'language';
  static const String userKey = 'user';
  static const String isLoggedInKey = 'isLoggedIn';
}