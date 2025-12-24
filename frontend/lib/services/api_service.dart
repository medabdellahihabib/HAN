import 'dart:convert';
import 'package:http/http.dart' as http;

class ApiService {
  // Pour Windows desktop
  static const String baseUrl = "http://127.0.0.1:8080/api";
  // Pour Android Emulator: http://10.0.2.2:8080/api
  // Pour téléphone réel: http://<IP_PC>:8080/api

  // GET /hello/
  static Future<String> getHello() async {
    final response = await http.get(Uri.parse("$baseUrl/hello/"));
    if (response.statusCode == 200) {
      return jsonDecode(response.body)['message'];
    } else {
      throw Exception("Failed to load hello");
    }
  }

  // POST /login/
  static Future<Map<String, dynamic>> login(String username, String password) async {
    final response = await http.post(
      Uri.parse("$baseUrl/login/"),
      headers: {"Content-Type": "application/json"},
      body: jsonEncode({"username": username, "password": password}),
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      return {"error": jsonDecode(response.body)['error']};
    }
  }

  // GET /home/ (auth required, session management simplifiée)
  static Future<String> getHome() async {
    final response = await http.get(Uri.parse("$baseUrl/home/"));
    if (response.statusCode == 200) {
      return jsonDecode(response.body)['message'];
    } else {
      throw Exception("Failed to load home");
    }
  }

  // POST /logout/
  static Future<void> logout() async {
    await http.post(Uri.parse("$baseUrl/logout/"));
  }
}
