class UserModel {
  final int id;
  final String username;
  final String firstName;
  final String lastName;
  final String phoneNumber;
  final String gender;
  final int age;
  final String languagePreference;
  final DateTime createdAt;

  UserModel({
    required this.id,
    required this.username,
    required this.firstName,
    required this.lastName,
    required this.phoneNumber,
    required this.gender,
    required this.age,
    required this.languagePreference,
    required this.createdAt,
  });

  factory UserModel.fromJson(Map<String, dynamic> json) {
    return UserModel(
      id: json['id'],
      username: json['username'],
      firstName: json['first_name'] ?? '',
      lastName: json['last_name'] ?? '',
      phoneNumber: json['phone_number'] ?? '',
      gender: json['gender'] ?? '',
      age: json['age'] ?? 0,
      languagePreference: json['language_preference'] ?? 'ar',
      createdAt: DateTime.parse(json['created_at']),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'username': username,
      'first_name': firstName,
      'last_name': lastName,
      'phone_number': phoneNumber,
      'gender': gender,
      'age': age,
      'language_preference': languagePreference,
      'created_at': createdAt.toIso8601String(),
    };
  }
}