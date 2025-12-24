//import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:flutter/material.dart';
import 'package:flutter_storage_app/database.dart';
import 'package:random_string/random_string.dart';

class AddDatabase extends StatefulWidget {
  const AddDatabase({super.key});

  @override
  State<AddDatabase> createState() => _AddDatabaseState();
}

class _AddDatabaseState extends State<AddDatabase> {
  TextEditingController nameController = TextEditingController();
  TextEditingController ageController = TextEditingController();
  TextEditingController genderController = TextEditingController();
  TextEditingController phoneController = TextEditingController();
  TextEditingController roomController = TextEditingController();
  TextEditingController diseaseController = TextEditingController();
  TextEditingController dateController = TextEditingController();
  TextEditingController timeController = TextEditingController();
  Stream? residentStream;


  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SingleChildScrollView(             
        child: Container(
        margin: EdgeInsets.only(top: 40.0, left: 30.0, right: 30.0, bottom: 40.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children:[
        Row(
            children: [
              GestureDetector(                  
                onTap: () => Navigator.pop(context),
                child: Icon(Icons.arrow_back_ios_new_outlined),
              ),
              SizedBox(width: 60.0,), // khoảng cách giữa icon và text
              Text(
                "Thêm hồ sơ", 
                style: TextStyle(
                  color: Colors.blue, 
                  fontSize: 26.0, 
                  fontWeight: FontWeight.bold)
                )
              ],
            ),
            SizedBox(height: 30.0,), // khoảng cách giữa các dòng
            Text(
                "Họ và tên", 
                style: TextStyle(
                  color: Colors.blue, 
                  fontSize: 20.0, 
                  fontWeight: FontWeight.bold)
                ),
                SizedBox(height: 10.0,),
                Container(
                  padding: EdgeInsets.only(left: 20.0),
                  decoration: BoxDecoration(
                    color: Color(0xFFececf8), borderRadius: BorderRadius.circular(10)
                  ),
                  child: TextField(
                    controller: nameController,
                    decoration: InputDecoration(
                      hintText: "Nhập Họ và tên",
                      border: InputBorder.none
                    ),
                  ),
                ),
                SizedBox(height: 30.0,),
                Text(
                "Ngày sinh", 
                style: TextStyle(
                  color: Colors.blue, 
                  fontSize: 20.0, 
                  fontWeight: FontWeight.bold)
                ),
                SizedBox(height: 10.0,),
                Container(
                  padding: EdgeInsets.only(left: 20.0),
                  decoration: BoxDecoration(
                    color: Color(0xFFececf8), borderRadius: BorderRadius.circular(10)
                  ),
                  child: TextField(
                    controller: ageController,
                    decoration: InputDecoration(
                      hintText: "Nhập Ngày sinh",
                      border: InputBorder.none
                    ),
                  ),
                ),
                SizedBox(height: 30.0,),
                Text(
                "Giới tính", 
                style: TextStyle(
                  color: Colors.blue, 
                  fontSize: 20.0, 
                  fontWeight: FontWeight.bold)
                ),
                SizedBox(height: 10.0,),
                Container(
                  padding: EdgeInsets.only(left: 20.0),
                  decoration: BoxDecoration(
                    color: Color(0xFFececf8), borderRadius: BorderRadius.circular(10)
                  ),
                  child: TextField(
                    controller: genderController,
                    decoration: InputDecoration(
                      hintText: "Nhập giới tính",
                      border: InputBorder.none
                    ),
                  ),
                ),
                SizedBox(height: 30.0,),
                Text(
                "Số điện thoại thân nhân", 
                style: TextStyle(
                  color: Colors.blue, 
                  fontSize: 20.0, 
                  fontWeight: FontWeight.bold)
                ),
                SizedBox(height: 10.0,),
                Container(
                  padding: EdgeInsets.only(left: 20.0),
                  decoration: BoxDecoration(
                    color: Color(0xFFececf8), borderRadius: BorderRadius.circular(10)
                  ),
                  child: TextField(
                    controller: phoneController,
                    decoration: InputDecoration(
                      hintText: "Nhập Số điện thoại",
                      border: InputBorder.none
                    ),
                  ),
                ),
                SizedBox(height: 30.0,),
                Text(
                "Phòng", 
                style: TextStyle(
                  color: Colors.blue, 
                  fontSize: 20.0, 
                  fontWeight: FontWeight.bold)
                ),
                SizedBox(height: 10.0,),
                Container(
                  padding: EdgeInsets.only(left: 20.0),
                  decoration: BoxDecoration(
                    color: Color(0xFFececf8), borderRadius: BorderRadius.circular(10)
                  ),
                  child: TextField(
                    controller: roomController,
                    decoration: InputDecoration(
                      hintText: "Nhập Số phòng",
                      border: InputBorder.none
                    ),
                  ),
                ),
                SizedBox(height: 30.0,),
                Text(
                "Bệnh nền", 
                style: TextStyle(
                  color: Colors.blue, 
                  fontSize: 20.0, 
                  fontWeight: FontWeight.bold)
                ),
                SizedBox(height: 10.0,),
                Container(
                  padding: EdgeInsets.only(left: 20.0),
                  decoration: BoxDecoration(
                    color: Color(0xFFececf8), borderRadius: BorderRadius.circular(10)
                  ),
                  child: TextField(
                    controller: diseaseController,
                    decoration: InputDecoration(
                      hintText: "Nhập Thông tin bệnh nền",
                      border: InputBorder.none
                    ),
                  ),
                ),
                SizedBox(height: 30.0,),
                Text(
                "Ngày uống", 
                style: TextStyle(
                  color: Colors.blue, 
                  fontSize: 20.0, 
                  fontWeight: FontWeight.bold)
                ),
                SizedBox(height: 10.0,),
                Container(
                  padding: EdgeInsets.only(left: 20.0),
                  decoration: BoxDecoration(
                    color: Color(0xFFececf8), borderRadius: BorderRadius.circular(10)
                  ),
                  child: TextField(
                    controller: dateController,
                    decoration: InputDecoration(
                      hintText: "Nhập Ngày uống thuốc",
                      border: InputBorder.none
                    ),
                  ),
                ),
                SizedBox(height: 30.0,),
                Text(
                "Giờ uống", 
                style: TextStyle(
                  color: Colors.blue, 
                  fontSize: 20.0, 
                  fontWeight: FontWeight.bold)
                ),
                SizedBox(height: 10.0,),
                Container(
                  padding: EdgeInsets.only(left: 20.0),
                  decoration: BoxDecoration(
                    color: Color(0xFFececf8), borderRadius: BorderRadius.circular(10)
                  ),
                  child: TextField(
                    controller: timeController,
                    decoration: InputDecoration(
                      hintText: "Nhập Giờ uống thuốc",
                      border: InputBorder.none
                    ),
                  ),
                ),
                SizedBox(height: 50.0,),
                GestureDetector(
                  onTap: ()async{
                    if(nameController.text != "" 
                    && ageController.text != "" 
                    && genderController.text != "" 
                    && phoneController.text != "" 
                    && roomController.text != "" 
                    && diseaseController.text != ""
                    && dateController.text != ""
                    && timeController.text != ""){
                      String addID = randomAlphaNumeric(10);
                      Map<String, dynamic> residentInfoMap = {
                        "name": nameController.text,
                        "age": ageController.text,
                        "gender": genderController.text,
                        "phone": phoneController.text,
                        "room": roomController.text,
                        "disease": diseaseController.text,
                        "date": dateController.text,
                        "time": timeController.text,
                        "done": false,
                        "not yet": false
                      };
                      await DatabaseMethods()
                        .addDatabase(residentInfoMap, addID)
                        .then((value) {
                          nameController.text = "";
                          ageController.text = "";
                          genderController.text = "";
                          phoneController.text = "";
                          roomController.text = "";
                          diseaseController.text = "";
                      ScaffoldMessenger.of(context).showSnackBar(SnackBar(
                        backgroundColor: Colors.green,
                          content:Text(
                            "Dữ liệu đã được thêm vào", 
                            style: TextStyle(
                              fontSize: 20.0, fontWeight: FontWeight.bold),)));
                      });
                      
                    }
                  },
                  child: Center(
                    child: Container(
                      padding: EdgeInsets.symmetric(vertical: 8.0),
                      width: 150,
                      decoration: BoxDecoration(
                        color: Colors.blue, borderRadius: BorderRadius.circular(10)),
                    alignment: Alignment.center,
                    child: Center(
                      child:Text(
                        "Thêm vào", 
                        style: TextStyle(
                          color: Colors.white,     
                          fontSize: 24.0, 
                          fontWeight: FontWeight.bold)
                        ),
                      ),
                  ), ),
                ),
      ],),),
    ),);
  }
}