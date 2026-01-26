import 'package:flutter/material.dart';
import '../models/henna_type_model.dart';
import '../models/order_model.dart';
import '../services/api_service.dart';

class HennaProvider with ChangeNotifier {
  final ApiService _apiService = ApiService();
  
  List<HennaTypeModel> _hennaTypes = [];
  List<OrderModel> _myOrders = [];
  bool _isLoading = false;
  String? _errorMessage;

  List<HennaTypeModel> get hennaTypes => _hennaTypes;
  List<OrderModel> get myOrders => _myOrders;
  bool get isLoading => _isLoading;
  String? get errorMessage => _errorMessage;

  // Fetch Henna Types
  Future<void> fetchHennaTypes() async {
    _isLoading = true;
    _errorMessage = null;
    notifyListeners();

    try {
      _hennaTypes = await _apiService.getHennaTypes();
      _isLoading = false;
      notifyListeners();
    } catch (e) {
      _errorMessage = e.toString().replaceAll('Exception: ', '');
      _isLoading = false;
      notifyListeners();
    }
  }

  // Create Order
  Future<bool> createOrder({
    required int hennaTypeId,
    String? notes,
    String? address,
  }) async {
    _isLoading = true;
    _errorMessage = null;
    notifyListeners();

    try {
      await _apiService.createOrder(
        hennaTypeId: hennaTypeId,
        notes: notes,
        address: address,
      );
      
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

  // Fetch My Orders
  Future<void> fetchMyOrders() async {
    _isLoading = true;
    _errorMessage = null;
    notifyListeners();

    try {
      _myOrders = await _apiService.getMyOrders();
      _isLoading = false;
      notifyListeners();
    } catch (e) {
      _errorMessage = e.toString().replaceAll('Exception: ', '');
      _isLoading = false;
      notifyListeners();
    }
  }

  void clearError() {
    _errorMessage = null;
    notifyListeners();
  }
}