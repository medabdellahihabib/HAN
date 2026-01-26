import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';
import '../utils/constants.dart';
import '../models/user_model.dart';
import '../models/henna_type_model.dart';
import '../models/order_model.dart';

class ApiService {
  final String baseUrl = AppConstants.baseUrl;
  
  // Récupérer les cookies de session
  Future<Map<String, String>> _getHeaders() async {
    final prefs = await SharedPreferences.getInstance();
    final cookies = prefs.getString('cookies') ?? '';
    
    return {
      'Content-Type': 'application/json',
      'Cookie': cookies,
    };
  }
  
  // Sauvegarder les cookies
  Future<void> _saveCookies(http.Response response) async {
    final prefs = await SharedPreferences.getInstance();
    final cookies = response.headers['set-cookie'];
    if (cookies != null) {
      await prefs.setString('cookies', cookies);
    }
  }

  // Register
  Future<Map<String, dynamic>> register({
    required String username,
    required String password,
    required String passwordConfirm,
    required String firstName,
    required String lastName,
    required String phoneNumber,
    required String gender,
    required int age,
    String languagePreference = 'ar',
  }) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl${AppConstants.registerEndpoint}'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'username': username,
          'password': password,
          'password_confirm': passwordConfirm,
          'first_name': firstName,
          'last_name': lastName,
          'phone_number': phoneNumber,
          'gender': gender,
          'age': age,
          'language_preference': languagePreference,
        }),
      );

      if (response.statusCode == 201) {
        await _saveCookies(response);
        return jsonDecode(response.body);
      } else {
        final error = jsonDecode(response.body);
        throw Exception(error['error'] ?? 'خطأ في التسجيل');
      }
    } catch (e) {
      throw Exception('فشل الاتصال بالخادم: $e');
    }
  }

  // Login
  Future<Map<String, dynamic>> login({
    required String username,
    required String password,
  }) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl${AppConstants.loginEndpoint}'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'username': username,
          'password': password,
        }),
      );

      if (response.statusCode == 200) {
        await _saveCookies(response);
        return jsonDecode(response.body);
      } else {
        final error = jsonDecode(response.body);
        throw Exception(error['error'] ?? 'خطأ في تسجيل الدخول');
      }
    } catch (e) {
      throw Exception('فشل الاتصال بالخادم: $e');
    }
  }

  // Get Henna Types
  Future<List<HennaTypeModel>> getHennaTypes() async {
    try {
      final headers = await _getHeaders();
      final response = await http.get(
        Uri.parse('$baseUrl${AppConstants.hennaTypesEndpoint}'),
        headers: headers,
      );

      if (response.statusCode == 200) {
        final List<dynamic> data = jsonDecode(response.body);
        return data.map((json) => HennaTypeModel.fromJson(json)).toList();
      } else {
        throw Exception('فشل في تحميل أنواع الحناء');
      }
    } catch (e) {
      throw Exception('فشل الاتصال بالخادم: $e');
    }
  }

  // Create Order
  Future<Map<String, dynamic>> createOrder({
    required int hennaTypeId,
    String? notes,
    String? address,
  }) async {
    try {
      final headers = await _getHeaders();
      final response = await http.post(
        Uri.parse('$baseUrl${AppConstants.createOrderEndpoint}'),
        headers: headers,
        body: jsonEncode({
          'henna_type': hennaTypeId,
          'notes': notes ?? '',
          'address': address ?? '',
        }),
      );

      if (response.statusCode == 201) {
        return jsonDecode(response.body);
      } else {
        final error = jsonDecode(response.body);
        throw Exception(error['error'] ?? 'فشل في إنشاء الطلب');
      }
    } catch (e) {
      throw Exception('فشل الاتصال بالخادم: $e');
    }
  }

  // Get My Orders
  Future<List<OrderModel>> getMyOrders() async {
    try {
      final headers = await _getHeaders();
      final response = await http.get(
        Uri.parse('$baseUrl${AppConstants.myOrdersEndpoint}'),
        headers: headers,
      );

      if (response.statusCode == 200) {
        final List<dynamic> data = jsonDecode(response.body);
        return data.map((json) => OrderModel.fromJson(json)).toList();
      } else {
        throw Exception('فشل في تحميل الطلبات');
      }
    } catch (e) {
      throw Exception('فشل الاتصال بالخادم: $e');
    }
  }

  // Change Language
  Future<void> changeLanguage(String language) async {
    try {
      final headers = await _getHeaders();
      await http.post(
        Uri.parse('$baseUrl${AppConstants.changeLanguageEndpoint}'),
        headers: headers,
        body: jsonEncode({'language': language}),
      );
    } catch (e) {
      throw Exception('فشل في تغيير اللغة: $e');
    }
  }

  // Logout
  Future<void> logout() async {
    try {
      final headers = await _getHeaders();
      await http.post(
        Uri.parse('$baseUrl${AppConstants.logoutEndpoint}'),
        headers: headers,
      );
      
      final prefs = await SharedPreferences.getInstance();
      await prefs.clear();
    } catch (e) {
      throw Exception('فشل في تسجيل الخروج: $e');
    }
  }
}