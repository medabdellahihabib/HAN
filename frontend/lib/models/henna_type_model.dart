class HennaTypeModel {
  final int id;
  final String name;
  final String description;
  final String imageUrl;
  final double price;
  final bool isAvailable;

  HennaTypeModel({
    required this.id,
    required this.name,
    required this.description,
    required this.imageUrl,
    required this.price,
    required this.isAvailable,
  });

  factory HennaTypeModel.fromJson(Map<String, dynamic> json) {
    return HennaTypeModel(
      id: json['id'],
      name: json['name'] ?? '',
      description: json['description'] ?? '',
      imageUrl: json['image_url'] ?? '',
      price: double.parse(json['price'].toString()),
      isAvailable: json['is_available'] ?? true,
    );
  }
}