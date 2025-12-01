import 'package:flutter/material.dart';
import 'package:flutter_storage_app/add.dart';
import 'package:flutter_storage_app/search.dart';
import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:flutter_storage_app/database.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:intl/intl.dart';

class Home extends StatefulWidget {
  const Home({super.key});

  @override
  State<Home> createState() => _HomeState();
}

class _HomeState extends State<Home> {

  @override
  void initState() {
    checkAndResetStatus();   // reset 1 lần mỗi ngày
    getontheload();
    super.initState();
  
  }

  getontheload(){
    residentStream = DatabaseMethods().getResidentDetails();
    setState(() {

    });

  }

  // Hàm kiểm tra ngày reset
  Future<void> checkAndResetStatus() async {
    final prefs = await SharedPreferences.getInstance();

    // Ngày hôm nay dạng yyyy-MM-dd
    String today = DateFormat('yyyy-MM-dd').format(DateTime.now());

    // Lấy ngày reset lần trước
    String? lastResetDate = prefs.getString('lastResetDate');

    if (lastResetDate != today) {
      // Nếu chưa reset trong ngày hôm nay -> reset
      await DatabaseMethods().resetAllStatus();

      // Lưu lại ngày reset hôm nay
      await prefs.setString('lastResetDate', today);

      // Hiện thông báo cho điều dưỡng
    if (mounted) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text("Đã cập nhật lại trạng thái cho ngày mới"),
          backgroundColor: Colors.green,
          duration: Duration(seconds: 2),
        ),
      );
     }
    }
  }

void updateStatus(String docId, String status) async {
  try {
    // Cập nhật cả 2 field, chỉ 1 cái true
    Map<String, dynamic> updateData = {};
    
    if (status == "done") {
      updateData = {
        'done': true,
        'not yet': false,
      };
    } else if (status == "not yet") {
      updateData = {
        'done': false,
        'not yet': true,
      };
    }
    
    await FirebaseFirestore.instance
        .collection('residentInfo')
        .doc(docId)
        .update(updateData);
    
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text("Đã cập nhật trạng thái!"),
        duration: Duration(seconds: 1),
      ),
    );
  } catch (e) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text("Lỗi: $e"),
        backgroundColor: Colors.red,
      ),
    );
  }
}
// Thêm function delete
void deleteResident(String docId, String patientName) async {
  // Hiển thị dialog xác nhận
  bool? shouldDelete = await showDialog<bool>(
    context: context,
    builder: (BuildContext context) {
      return AlertDialog(
        title: Text("Xác nhận xóa"),
        content: Text("Bạn có chắc chắn muốn xóa thông tin bệnh nhân $patientName?"),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(context).pop(false),
            child: Text("Hủy"),
          ),
          TextButton(
            onPressed: () => Navigator.of(context).pop(true),
            child: Text("Xóa", style: TextStyle(color: Colors.red)),
          ),
        ],
      );
    },
  );

  if (shouldDelete == true) {
    try {
      await DatabaseMethods().deleteResident(docId);
      
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text("Đã xóa thông tin bệnh nhân!"),
          duration: Duration(seconds: 2),
        ),
      );
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text("Lỗi khi xóa: $e"),
          backgroundColor: Colors.red,
        ),
      );
    }
  }
}

  Stream<QuerySnapshot<Map<String, dynamic>>>? residentStream;


Widget showResidentList(){
return StreamBuilder<QuerySnapshot<Map<String, dynamic>>>(
  stream: residentStream,
  builder: (context, snapshot){
    if (snapshot.hasError) {
      return Center(child: Text("Lỗi: ${snapshot.error}"),);
    }
    if (snapshot.connectionState == ConnectionState.waiting) {
      return Center(child: CircularProgressIndicator(),);
    }
    if (!snapshot.hasData || snapshot.data!.docs.isEmpty) {
      return Center(child: Text("Chưa có dữ liệu"),);
    }

    return ListView.builder(
      padding: EdgeInsets.zero,
      shrinkWrap: true,
      scrollDirection: Axis.vertical,
      itemCount: snapshot.data?.docs.length ?? 0,
      itemBuilder: (context, index) {
        DocumentSnapshot<Map<String, dynamic>> ds = 
            snapshot.data!.docs[index];
        var data = ds.data()!;
        String docId = ds.id;

        return Container(
            margin: const EdgeInsets.symmetric(horizontal: 20.0, vertical: 10.0),
            child: Material(
            elevation: 3.0,
            borderRadius: BorderRadius.circular(10),
            child: Container(
              padding: EdgeInsets.only(left: 20.0, top: 10.0, bottom: 10.0, right: 20.0),              
              decoration: BoxDecoration(color: Colors.white, borderRadius: BorderRadius.circular(10)),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                       Row(
                          children: [
                            const Text(
                              "Họ và tên : ",
                              style: TextStyle(
                                color: Colors.black,
                                fontSize: 17.0,
                                fontWeight: FontWeight.w500,
                              ),
                            ),
                            Flexible(
                              child: Container(
                                margin: EdgeInsets.only(right: 30), // để chỗ cho icon
                                child: Text(
                                  data["name"] ?? "N/A",
                                  maxLines: 1,
                                  overflow: TextOverflow.ellipsis,
                                  style: const TextStyle(
                                    color: Colors.blue,
                                    fontSize: 19.0,
                                    fontWeight: FontWeight.bold,
                                  ),
                                ),
                              ),
                            ),
                            
                            Positioned(
                                top: 0,
                                right: -20,
                                child:GestureDetector(
                                  onTap: () => deleteResident(docId, data["name"] ?? ""),
                                  child: const Icon(
                                    Icons.delete,
                                    color: Colors.black,
                                    size: 26,
                                  ),
                                ),
                            ),
                        ],
                      ),

                      const SizedBox(height: 5.0),
                      Row(
                        children: [
                          const Text(
                            "Ngày sinh : ",
                            style: TextStyle(
                              color: Colors.black,
                              fontSize: 17.0,
                              fontWeight: FontWeight.w500,
                            ),
                          ),
                          Flexible(
                            child: Text(
                              data["age"] ?? "N/A",
                              overflow: TextOverflow.ellipsis,
                              style: const TextStyle(
                                color: Colors.blue,
                                fontSize: 19.0,
                                fontWeight: FontWeight.bold,
                              ),
                            ),
                          ),
                        ],
                      ),
                      const SizedBox(height: 5.0),
                      Row(
                        children: [
                          const Text(
                            "Giới tính : ",
                            style: TextStyle(
                              color: Colors.black,
                              fontSize: 17.0,
                              fontWeight: FontWeight.w500,
                            ),
                          ),
                          Flexible(
                            child: Text(
                              data["gender"] ?? "N/A",
                              overflow: TextOverflow.ellipsis,
                              style: const TextStyle(
                                color: Colors.blue,
                                fontSize: 19.0,
                                fontWeight: FontWeight.bold,
                              ),
                            ),
                          ),
                        ],
                      ),
                      const SizedBox(height: 5.0),
                      Row(
                        children: [
                          const Text(
                            "Số điện thoại thân nhân : ",
                            style: TextStyle(
                              color: Colors.black,
                              fontSize: 17.0,
                              fontWeight: FontWeight.w500,
                            ),
                          ),
                          Flexible(
                            child: Text(
                              data["phone"] ?? "N/A",
                              overflow: TextOverflow.ellipsis,
                              style: const TextStyle(
                                color: Colors.blue,
                                fontSize: 19.0,
                                fontWeight: FontWeight.bold,
                              ),
                            ),
                          ),
                        ],
                      ),
                      const SizedBox(height: 5.0),
                      Row(
                        children: [
                          const Text(
                            "Phòng : ",
                            style: TextStyle(
                              color: Colors.black,
                              fontSize: 17.0,
                              fontWeight: FontWeight.w500,
                            ),
                          ),
                          Flexible(
                            child: Text(
                              data["room"] ?? "N/A",
                              overflow: TextOverflow.ellipsis,
                              style: const TextStyle(
                                color: Colors.blue,
                                fontSize: 19.0,
                                fontWeight: FontWeight.bold,
                              ),
                            ),
                          ),
                        ],
                      ),
                      const SizedBox(height: 5.0),
                      Row(
                        children: [
                          const Text(
                            "Bệnh nền : ",
                            style: TextStyle(
                              color: Colors.black,
                              fontSize: 17.0,
                              fontWeight: FontWeight.w500,
                            ),
                          ),
                          Flexible(
                            child: Text(
                              data["disease"] ?? "N/A",
                              overflow: TextOverflow.ellipsis,
                              style: const TextStyle(
                                color: Colors.blue,
                                fontSize: 19.0,
                                fontWeight: FontWeight.bold,
                              ),
                            ),
                          ),
                        ],
                      ),
                      const SizedBox(height: 5.0),
                      Row(
                        children: [
                          const Text(
                            "Lịch uống thuốc : ",
                            style: TextStyle(
                              color: Colors.black,
                              fontSize: 17.0,
                              fontWeight: FontWeight.w500,
                            ),
                          ),
                          Flexible(
                            child: Text(
                              data["date"] ?? "N/A",
                              overflow: TextOverflow.ellipsis,
                              style: const TextStyle(
                                color: Colors.blue,
                                fontSize: 19.0,
                                fontWeight: FontWeight.bold,
                              ),
                            ),
                          ),
                        ],
                      ),
                      const SizedBox(height: 5.0),
                      Row(
                        children: [
                          const Text(
                            "Giờ uống thuốc : ",
                            style: TextStyle(
                              color: Colors.black,
                              fontSize: 17.0,
                              fontWeight: FontWeight.w500,
                            ),
                          ),
                          Flexible(
                            child: Text(
                              data["time"] ?? "N/A",
                              overflow: TextOverflow.ellipsis,
                              style: const TextStyle(
                                color: Colors.blue,
                                fontSize: 19.0,
                                fontWeight: FontWeight.bold,
                              ),
                            ),
                          ),
                        ],
                      ),
       

                      SizedBox(height: 10.0,),
                  //Thêm trạng thái cho mỗi bệnh nhân
                      Row(
                        children: [ 
                          Text(
                            "Trạng thái: ",
                            style: TextStyle(
                              color: Colors.black,
                              fontSize: 16.0,
                              fontWeight: FontWeight.w500
                            ),
                          ),
                          SizedBox(width: 10.0),
                          // Button (O)
                              GestureDetector(
                                onTap: () => updateStatus(docId, "done"),
                                child: Container(
                                  width: 40,
                                  height: 40,
                                  margin: EdgeInsets.only(right: 10.0),
                                  decoration: BoxDecoration(
                                    color: (data["done"] == true) ? Colors.green : Colors.grey[300],
                                    borderRadius: BorderRadius.circular(5),
                                    border: Border.all(
                                      color: (data["done"] == true) ? Colors.green : Colors.grey,
                                      width: 2
                                    )
                                  ),
                                  child: Center(
                                    child: Text(
                                      "O",
                                      style: TextStyle(
                                        color: (data["done"] == true) ? Colors.white : Colors.grey[600],
                                        fontSize: 16.0,
                                        fontWeight: FontWeight.bold
                                      ),
                                    ),
                                  ),
                                ),
                              ),
                              // Button (X)
                              GestureDetector(
                                onTap: () => updateStatus(docId, "not yet"),
                                child: Container(
                                  width: 40,
                                  height: 40,
                                  decoration: BoxDecoration(
                                    color: (data["not yet"] == true) ? Colors.red : Colors.grey[300],
                                    borderRadius: BorderRadius.circular(5),
                                    border: Border.all(
                                      color: (data["not yet"] == true) ? Colors.red : Colors.grey,
                                      width: 2
                                    )
                                  ),
                                  child: Center(
                                    child: Text(
                                      "X",
                                      style: TextStyle(
                                        color: (data["not yet"] == true) ? Colors.white : Colors.grey[600],
                                        fontSize: 16.0,
                                        fontWeight: FontWeight.bold
                                      ),
                                    ),
                                  ),
                                ),
                              ),
                            ],
                          ),
                        ], //children
                      ), 
              ),
        ),
       );
      },
    );
  },
);
}

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      floatingActionButton: Row(
      mainAxisAlignment: MainAxisAlignment.end, // đẩy về bên phải
      children: [
        // Nút search (kính lúp)
        FloatingActionButton(
          heroTag: "btnSearch", // heroTag khác nhau để tránh lỗi
          backgroundColor: Colors.blue,
          onPressed: () {
            Navigator.push(
              context,
              MaterialPageRoute(builder: (context) => SearchPage()), 
            );
          },
          child: Icon(Icons.search, color: Colors.white),
        ),
        SizedBox(width: 15), // khoảng cách giữa 2 nút

        // Nút thêm (+)
        FloatingActionButton(
          heroTag: "btnAdd",
          backgroundColor: Colors.blue,
          onPressed: () {
            Navigator.push(
              context,
              MaterialPageRoute(builder: (context) => AddDatabase()),
            );
          },
          child: Icon(Icons.add, color: Colors.white),
        ),
      ],
    ),
      body: Container(
        margin: EdgeInsets.only(top: 40.0, left: 20.0, right: 20.0),
        child: Column(
          children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Text(
                "Hồ sơ bệnh nhân", 
                style: TextStyle(
                  color: Colors.blue, 
                  fontSize: 26.0, 
                  fontWeight: FontWeight.bold)
                )
              ],
            ),
                  
            SizedBox(height: 20.0,),
            Expanded(child: showResidentList()),
          ],
        ),
      ),
    );
  }
}
