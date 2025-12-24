import 'package:flutter/material.dart';
import 'package:cloud_firestore/cloud_firestore.dart';

class SearchPage extends StatefulWidget {
  const SearchPage({super.key});

  @override
  _SearchPageState createState() => _SearchPageState();
}

class _SearchPageState extends State<SearchPage> {
  TextEditingController searchController = TextEditingController();
  Map<String, dynamic>? searchResult;

  void searchPatient() async {
    String name = searchController.text.trim();

    if (name.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text("Vui lòng nhập tên bệnh nhân")),
      );
      return;
    }

    try {
      var query = await FirebaseFirestore.instance
          .collection("residentInfo")
          .where("name", isEqualTo: name)
          .get();

      if (query.docs.isNotEmpty) {
        setState(() {
          searchResult = query.docs.first.data();
        });
      } else {
        setState(() {
          searchResult = null;
        });
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text("Không tìm thấy bệnh nhân")),
        );
      }
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text("Lỗi khi tìm: $e")),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
  appBar: AppBar(
    backgroundColor: Colors.transparent,
    elevation: 0,
    centerTitle: true,
    toolbarHeight: kToolbarHeight + 30, // tăng chiều cao AppBar để tạo khoảng trống trên
    title: Padding(
      padding: const EdgeInsets.only(top: 20), // chỉnh khoảng cách chữ với mép trên AppBar
      child: Text(
        "Tìm kiếm bệnh nhân",
        style: TextStyle(
          color: Colors.blue,
          fontSize: 26.0,
          fontWeight: FontWeight.bold,
        ),
      ),
    ),
  ),

      body: Padding(
        padding: const EdgeInsets.all(30.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              "Nhập họ và tên",
              style: TextStyle(
                  color: Colors.blue, 
                  fontSize: 22.0, 
                  fontWeight: FontWeight.bold)
            ),
            SizedBox(height: 10),
            TextField(
              controller: searchController,
              decoration: InputDecoration(
                hintText: "Ví dụ: Nguyễn Văn A",
                filled: true,
                fillColor: Colors.blue.shade100,
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(10),
                  borderSide: BorderSide.none,
                ),
              ),
            ),
            SizedBox(height: 20),
            Center(
              child: ElevatedButton(
                onPressed: searchPatient,
                style: ElevatedButton.styleFrom(
                  backgroundColor: Colors.blue,
                  padding: EdgeInsets.symmetric(horizontal: 40, vertical: 15),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(10),
                  ),
                ),
                child: Text(
                  "Tìm kiếm",
                  style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: Colors.white),
                ),
              ),
            ),
            SizedBox(height: 30),

            // Hiển thị kết quả
            if (searchResult != null) ...[
              Text(
                "Kết quả:",
                style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
              ),
              SizedBox(height: 10),
              Card(
                elevation: 3,
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(10),
                ),
                child: Padding(
                  padding: const EdgeInsets.all(15.0),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text("Họ và tên: ${searchResult!['name']}"),
                      Text("Ngày sinh: ${searchResult!['age']}"),
                      Text("Giới tính: ${searchResult!['gender']}"),
                      Text("SĐT thân nhân: ${searchResult!['phone']}"),
                      Text("Phòng: ${searchResult!['room']}"),
                      Text("Bệnh nền: ${searchResult!['disease']}"),
                      Text("Lịch uống: ${searchResult!['date']}"),
                      Text("Giờ uống: ${searchResult!['time']}"),
                    ],
                  ),
                ),
              ),
            ]
          ],
        ),
      ),
    );
  }
}
