# 📘 เว็บไซต์รายงานการพัฒนางานตามข้อตกลง (PA) ประจำปีงบประมาณ ๒๕๖๘
### นายอนันตชัย เพ็ชรรี่ (ครูเจมส์) | ตำแหน่ง ครู อันดับ คศ.๑
**โรงเรียนบ้านคลองมดแดง สำนักงานเขตพื้นที่การศึกษาประถมศึกษากำแพงเพชร เขต ๒**

---

## 🌟 จุดเด่นของโปรเจกต์
- 🎨 **Modern Official Design:** โทนสีน้ำเงิน-ขาว สไตล์ราชการพรีเมียม สวยงาม ทรงพลัง และทันสมัย
- ⚡ **Interactive Data Visualization:** กราฟสรุปผลคะแนน Pre/Post-test ด้วย Chart.js และสถิติ Paired t-test
- 📸 **Google Photos Live Evidence:** คลังภาพถ่ายเชิงประจักษ์จาก Google Photos พร้อม Lightbox ขยายภาพคมชัด
- 🔥 **Firebase Database Integration:** 
  - สถิติผู้เข้าชมแบบ Real-time (Visitor Counter)
  - แบบฟอร์มบันทึกข้อคิดเห็นและประเมินผลจากคณะกรรมการ (Committee Evaluation & Live Feedback Wall)
- 🚀 **Vercel Ready:** รองรับการ Deploy อัตโนมัติด้วย Vercel ภายใน 1 นาทีผ่าน GitHub

---

## 🚀 ขั้นตอนการเชื่อมต่อ GitHub และขึ้น Vercel

### ขั้นตอนที่ ๑ : สร้าง Repository บน GitHub และ Push โค้ด
1. ไปที่ [GitHub.com](https://github.com/new) แล้วกดสร้าง Repository ใหม่ (เช่น `pa-krujames-portfolio`) ตั้งค่าเป็น **Public**
2. เปิด PowerShell ในโฟลเดอร์นี้ แล้วรันคำสั่ง:
```bash
git add .
git commit -m "feat: complete modern official PA web portal with Firebase integration"
git branch -M main
git remote add origin https://github.com/YOUR_GITHUB_USERNAME/pa-krujames-portfolio.git
git push -u origin main
```

---

### ขั้นตอนที่ ๒ : Deploy บน Vercel (ฟรี 100%)
1. ไปที่ [Vercel.com](https://vercel.com/) แล้วล็อกอินด้วยบัญชี **GitHub**
2. คลิกปุ่ม **"Add New..."** > **"Project"**
3. เลือก Repository `pa-krujames-portfolio` ที่เพิ่ง Push ไป
4. ในหน้า Configure Project ให้คงค่า Default ไว้ทั้งหมด แล้วกด **"Deploy"**
5. รอประมาณ 30 วินาที จะได้โดเมนออนไลน์ฟรีทันที เช่น `https://pa-krujames-portfolio.vercel.app` 🎉

---

### ขั้นตอนที่ ๓ : การตั้งค่าฐานข้อมูล Firebase (ไม่บังคับ - มี Local Demo Mode ในตัว)
หากต้องการให้ข้อคิดเห็นและจำนวนผู้เข้าชมบันทึกลง Google Cloud Firebase แบบออนไลน์จริง:
1. ไปที่ [Firebase Console](https://console.firebase.google.com/)
2. สร้างโปรเจกต์ใหม่ (เช่น `pa-krujames`)
3. เมนู **Build** > **Firestore Database** > กด **Create Database** (เลือก **Start in test mode**)
4. ไปที่ **Project Settings (รูปเฟือง)** > ด้านล่างเลือก **Web App (</>)**
5. คัดลอกค่า `firebaseConfig` มาวางในไฟล์ `firebase-config.js`
6. รันคำสั่ง `git commit -am "chore: add firebase config"` และ `git push` Vercel จะอัปเดตระบบฐานข้อมูลให้ทันที!

---
© 2568–2569 โรงเรียนบ้านคลองมดแดง สพป.กำแพงเพชร เขต ๒
