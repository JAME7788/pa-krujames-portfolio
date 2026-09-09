// =========================================================================
// ฐานข้อมูล FIREBASE CONFIGURATION (ครูเจมส์ อนันตชัย เพ็ชรรี่)
// =========================================================================
// วิธีการเชื่อมต่อ:
// 1. ไปที่ https://console.firebase.google.com/
// 2. สร้างโปรเจกต์ใหม่ (เช่น pa-krujames)
// 3. ไปที่ Project Settings > ด้านล่างเลือก Web App (</>) > คัดลอกค่า firebaseConfig มาวางแทนที่ด้านล่างนี้
// 4. ไปที่เมนู Build > Firestore Database > คลิก Create database (เลือกโหมด Test mode เพื่อให้เขียนอ่านได้ทันที)
// 5. เมื่อบันทึกไฟล์นี้และอัปโหลดขึ้น GitHub/Vercel เว็บไซต์จะเชื่อมต่อฐานข้อมูลจริงทันที!
// =========================================================================

const firebaseConfig = {
  apiKey: "YOUR_FIREBASE_API_KEY",
  authDomain: "pa-krujames.firebaseapp.com",
  projectId: "pa-krujames",
  storageBucket: "pa-krujames.appspot.com",
  messagingSenderId: "123456789012",
  appId: "1:123456789012:web:abcdef1234567890"
};

// ตรวจสอบว่าครูเจมส์ใส่คีย์จริงแล้วหรือยัง
const isFirebaseConfigured = () => {
  return firebaseConfig.apiKey && firebaseConfig.apiKey !== "YOUR_FIREBASE_API_KEY";
};
