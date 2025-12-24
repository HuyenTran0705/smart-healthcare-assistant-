import 'dart:async';
// ignore: avoid_web_libraries_in_flutter
import 'dart:html' as html; // Thư viện để giao tiếp với JS trên Web
import 'dart:ui_web' as ui_web; // Thư viện để hiển thị HTML (Flutter 3.x trở lên)
import 'package:flutter/material.dart';
import 'package:firebase_core/firebase_core.dart';
import 'firebase_options.dart';
import 'package:flutter_storage_app/home.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Firebase.initializeApp(
    options: DefaultFirebaseOptions.currentPlatform,
  );
  
  // 1. Đăng ký cái "khung" hiển thị Web Robot
  // Lưu ý: Đường dẫn phải là cổng 5500 của Live Server
  ui_web.platformViewRegistry.registerViewFactory(
    'robot-view',
    (int viewId) => html.IFrameElement()
      ..src = 'http://127.0.0.1:5500/index.html' // <--- ĐỊA CHỈ ROBOT
      ..style.border = 'none'
      ..style.height = '100%'
      ..style.width = '100%',
  );

  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});
  @override
  Widget build(BuildContext context) {
    return const MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Firebase CRUD',
      home: RobotScreen(), // Chạy màn hình Robot trước
    );
  }
}

// === MÀN HÌNH ROBOT (FLUTTER WEB) ===
class RobotScreen extends StatefulWidget {
  const RobotScreen({super.key});

  @override
  State<RobotScreen> createState() => _RobotScreenState();
}

class _RobotScreenState extends State<RobotScreen> {
  late StreamSubscription _messageSubscription;

  @override
  void initState() {
    super.initState();
    // 2. Lắng nghe tín hiệu từ Robot gửi sang
    _messageSubscription = html.window.onMessage.listen((event) {
      // Nếu nhận được tín hiệu 'open_management_ui'
      if (event.data == 'open_management_ui') {
        print("Nhận được lệnh từ Robot -> Chuyển trang!");
        
        // Chuyển sang màn hình Quản lý (Home)
        Navigator.pushReplacement(
          context,
          MaterialPageRoute(builder: (context) => const Home()),
        );
      }
    });
  }

  @override
  void dispose() {
    _messageSubscription.cancel(); // Hủy lắng nghe khi thoát
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return const Scaffold(
      backgroundColor: Colors.white,
      // 3. Hiển thị cái khung Robot đã đăng ký ở trên
      body: HtmlElementView(viewType: 'robot-view'),
    );
  }
}