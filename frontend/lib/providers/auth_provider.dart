import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../models/user_model.dart';
import '../services/api_service.dart';
import 'dart:convert';

class AuthProvider with ChangeNotifier {
  final ApiService _apiService = ApiService();
  
  UserModel? _user;
  bool _isLoading = false;
  String? _errorMessage;
  Locale _locale = const Locale('ar');

  UserModel? get user => _user;
  bool get isLoading => _isLoading;
  String? get errorMessage => _errorMessage;
  Locale get locale => _locale;
  bool get isAuthenticated => _user != null;

  // Initialize - Check if user is logged in
  Future<void> initialize() async {
    final prefs = await SharedPreferences.getInstance();
    final userJson = prefs.getString(AppConstants.userKey);
    final language = prefs.getString(AppConstants.languageKey) ?? 'ar';
    
    if (userJson != null) {
      _user = UserModel.fromJson(jsonDecode(userJson));
    }
    
    _locale = Locale(language);
    notifyListeners();
  }

  // Register
  Future<bool> register({
    required String username,
    required String password,
    required String passwordConfirm,
    required String firstName,
    required String lastName,
    required String phoneNumber,
    required String gender,
    required int age,
  }) async {
    _isLoading = true;
    _errorMessage = null;
    notifyListeners();

    try {
      final response = await _apiService.register(
        username: username,
        password: password,
        passwordConfirm: passwordConfirm,
        firstName: firstName,
        lastName: lastName,
        phoneNumber: phoneNumber,
        gender: gender,
        age: age,
        languagePreference: _locale.languageCode,
      );

      _user = UserModel.fromJson(response['user']);
      
      // Save user data
      final prefs = await SharedPreferences.getInstance();
      await prefs.setString(AppConstants.userKey, jsonEncode(_user!.toJson()));
      await prefs.setBool(AppConstants.isLoggedInKey, true);

      _isLoading = false;
      notifyListeners();
      return true;
    } catch (e) {
      _errorMessage = e.toString().replaceAll('Exception: ', '');
      _isLoading = false;
      notifyListeners();
      return false;
    }
  }

  // Login
  Future<bool> login({
    required String username,
    required String password,
  }) async {
    _isLoading = true;
    _errorMessage = null;
    notifyListeners();

    try {
      final response = await _apiService.login(
        username: username,
        password: password,
      );

      _user = UserModel.fromJson(response['user']);
      
      // Save user data
      final prefs = await SharedPreferences.getInstance();
      await prefs.setString(AppConstants.userKey, jsonEncode(_user!.toJson()));
      await prefs.setBool(AppConstants.isLoggedInKey, true);

      _isLoading = false;
      notifyListeners();
      return true;
    } catch (e) {
      _errorMessage = e.toString().replaceAll('Exception: ', '');
      _isLoading = false;
      notifyListeners();
      return false;
    }
  }

  // Logout
  Future<void> logout() async {
    _isLoading = true;
    notifyListeners();

    try {
      await _apiService.logout();
      _user = null;
      
      final prefs = await SharedPreferences.getInstance();
      await prefs.clear();
      
      _isLoading = false;
      notifyListeners();
    } catch (e) {
      _isLoading = false;
      notifyListeners();
    }
  }

  // Change Language
  Future<void> changeLanguage(String languageCode) async {
    try {
      _locale = Locale(languageCode);
      
      final prefs = await SharedPreferences.getInstance();
      await prefs.setString(AppConstants.languageKey, languageCode);
      
      if (_user != null) {
        await _apiService.changeLanguage(languageCode);
      }
      
      notifyListeners();
    } catch (e) {
      print('Error changing language: $e');
    }
  }

  void clearError() {
    _errorMessage = null;
    notifyListeners();
  }
}