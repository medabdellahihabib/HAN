class OrderModel {
  final int id;
  final String clientName;
  final String clientPhone;
  final String hennaName;
  final double hennaPrice;
  final String status;
  final String statusDisplay;
  final String notes;
  final String address;
  final DateTime createdAt;

  OrderModel({
    required this.id,
    required this.clientName,
    required this.clientPhone,
    required this.hennaName,
    required this.hennaPrice,
    required this.status,
    required this.statusDisplay,
    required this.notes,
    required this.address,
    required this.createdAt,
  });

  factory OrderModel.fromJson(Map<String, dynamic> json) {
    return OrderModel(
      id: json['id'],
      clientName: json['client_name'] ?? '',
      clientPhone: json['client_phone'] ?? '',
      hennaName: json['henna_name'] ?? '',
      hennaPrice: double.parse(json['henna_price'].toString()),
      status: json['status'] ?? '',
      statusDisplay: json['status_display'] ?? '',
      notes: json['notes'] ?? '',
      address: json['address'] ?? '',
      createdAt: DateTime.parse(json['created_at']),
    );
  }
}