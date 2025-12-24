// import 'package:firebase_core/firebase_core.dart';
import 'package:cloud_firestore/cloud_firestore.dart';

class DatabaseMethods {
  Future addDatabase(Map<String, dynamic> residentInfoMap, String id) async {
    return await FirebaseFirestore.instance
    .collection("residentInfo")
    .doc(id)
    .set(residentInfoMap);
    
  }

  Stream<QuerySnapshot<Map<String, dynamic>>> getResidentDetails(){
    return FirebaseFirestore.instance
      .collection("residentInfo")
      .snapshots();
  }

  Future deleteResident(String id) async {
    return await FirebaseFirestore.instance
      .collection("residentInfo")
      .doc(id)
      .delete();
  }

  Future<void> resetAllStatus() async {
    final snapshot = await FirebaseFirestore.instance
        .collection("residentInfo")
        .get();

    for (var doc in snapshot.docs) {
      await doc.reference.update({
        "done": false,
        "not yet": false,
      });
    }
  }
}