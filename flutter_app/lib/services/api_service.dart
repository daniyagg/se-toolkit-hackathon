import 'dart:convert';
import 'package:http/http.dart' as http;

class ApiService {
  static const String baseUrl = 'http://10.93.25.142:8000';

  static Future<Map<String, dynamic>> getTodayWater(String userId) async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/water/today/$userId'),
      );
      if (response.statusCode == 200) {
        return json.decode(response.body);
      } else {
        throw Exception('Failed to load today\'s water data');
      }
    } catch (e) {
      throw Exception('Error fetching data: $e');
    }
  }

  static Future<Map<String, dynamic>> drinkWater(String userId) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/water/drink/$userId'),
      );
      if (response.statusCode == 200) {
        return json.decode(response.body);
      } else {
        throw Exception('Failed to record water intake');
      }
    } catch (e) {
      throw Exception('Error recording drink: $e');
    }
  }
}
