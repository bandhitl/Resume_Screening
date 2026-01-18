# 🚀 Deploy to Render.com - Step by Step Guide

## แบบที่ 1: ปล่อยให้ User ใส่ API Key เอง (แนะนำ)

### Step 1: Push Code to GitHub

1. **สร้าง Repository ใหม่บน GitHub**
   - เข้าไปที่ https://github.com/new
   - ตั้งชื่อ repo เช่น `resume-screener-pwa`
   - ไม่ต้องติ๊ก "Initialize with README" (เพราะมีอยู่แล้ว)

2. **Push code ไป GitHub** (ใน terminal)

```bash
cd /Users/banditl.lertpalanan/Desktop/Claude_Projects/Resume_screening

# Initialize git (ถ้ายังไม่ได้)
git init

# Add all files
git add .

# Commit
git commit -m "Convert to PWA with mobile optimization"

# Add remote
git remote add origin https://github.com/YOUR_USERNAME/resume-screener-pwa.git

# Push
git push -u origin main
```

### Step 2: Deploy บน Render.com

1. **เข้าไปที่** https://render.com

2. **Sign Up / Login**
   - ใช้ GitHub account ล็อกอิน (ง่ายที่สุด)

3. **สร้าง Web Service ใหม่**
   - คลิกปุ่ม **"New +"** → เลือก **"Web Service"**
   - เลือก GitHub repo ที่สร้างไว้
   - คลิก **"Connect"**

4. **Configure Service**
   - **Name**: `resume-screener-pwa` (หรือชื่ออื่น)
   - **Region**: Singapore (ใกล้ไทยสุด)
   - **Branch**: `main`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`

5. **Environment Variables** (สำคัญ!)
   คลิก **"Advanced"** → **"Add Environment Variable"**

   ```
   FLASK_SECRET_KEY = (ใส่ secret key ของคุณ หรือให้ Render generate)
   APP_PASSWORD = admin123 (หรือรหัสที่คุณต้องการ)
   ```

   **หมายเหตุ:** ยังไม่ต้องใส่ API Key ตรงนี้ (User จะใส่เองตอนใช้)

6. **Deploy**
   - คลิก **"Create Web Service"**
   - รอสักครู่ (ประมาณ 3-5 นาที)
   - Render จะให้ URL เช่น `https://resume-screener-pwa.onrender.com`

### Step 3: ทดสอบ PWA

1. **เปิด app** ด้วย URL ที่ Render ให้
2. **Login** ด้วย password ที่ตั้งไว้
3. **ใส่ API Key** ของคุณ (Anthropic หรือ OpenAI)
4. **Install บนมือถือ**
   - **Android**: Chrome menu → "Install app"
   - **iOS**: Safari → Share → "Add to Home Screen"

---

## แบบที่ 2: ใส่ API Key ใน Render (ถ้าอยากให้ User ไม่ต้องใส่)

### ขั้นตอนเพิ่มเติม:

1. **แก้โค้ดเพิ่ม** (แจ้งให้ผมทำให้)

2. **ใส่ Environment Variables ใน Render:**
   ในหน้า deploy เพิ่ม:
   ```
   ANTHROPIC_API_KEY = sk-ant-xxxxx... (API key ของคุณ)
   หรือ
   OPENAI_API_KEY = sk-proj-xxxxx... (API key ของคุณ)
   ```

3. **Redeploy** อีกครั้ง

---

## 💰 ค่าใช้จ่าย

### Render.com Free Tier:
- ✅ **ฟรี** แต่มีข้อจำกัด:
  - หยุดทำงานเมื่อไม่มีคนใช้ 15 นาที
  - ตื่นเองเมื่อมีคนเข้า (ใช้เวลา ~30-90 วินาที)
  - จำกัด 750 ชั่วโมง/เดือน

### Render.com Paid Tier:
- 💵 **$7/เดือน** (สำหรับ instance เล็ก)
  - ทำงาน 24/7
  - ไม่มีการ sleep
  - เหมาะสำหรับ production

---

## 🔧 Troubleshooting

### App ไม่หยุด sleep
แก้ไข: Upgrade เป็น paid tier หรือใช้ **Cron Job** ปลุกทุก 10 นาที

### ใส่ API Key แล้วยัง error
- เช็คว่าใส่ถูกต้องไหม
- เช็ค console บน browser (F12)
- ดู logs บน Render dashboard

### Service Worker ไม่ทำงาน
- ต้องใช้ **HTTPS** (Render ให้ฟรีอยู่แล้ว)
- Clear cache: Chrome DevTools → Application → Clear storage

---

## 📱 ติดตั้งบนมือถือ

### Android:
1. เปิดใน Chrome
2. แตะ menu (3 จุด)
3. เลือก "Install app" หรือ "Add to Home Screen"

### iOS:
1. เปิดใน Safari (**ต้อง Safari เท่านั้น**)
2. แตะปุ่ม Share
3. เลื่อนลง → "Add to Home Screen"
4. แตะ "Add"

---

## ✅ Checklist ก่อน Deploy

- [ ] Push code ไป GitHub แล้ว
- [ ] Sign up บน Render.com
- [ ] Connect GitHub repo
- [ ] Set Environment Variables (FLASK_SECRET_KEY, APP_PASSWORD)
- [ ] Deploy สำเร็จ
- [ ] Test URL ว่าใช้งานได้
- [ ] Test login ด้วย password
- [ ] Test ใส่ API Key และวิเคราะห์ resume
- [ ] Install บนมือถือ

---

## 🎯 ถ้าอยากเปลี่ยนให้ใส่ API Key ใน Render ทีหลัง

แจ้งให้ผมทำได้เลยครับ ผมจะแก้โค้ดให้:
1. สร้าง endpoint สำหรับดึง default API key
2. แก้ frontend ให้ไม่ต้องใส่ API key ถ้ามี default
3. อธิบายวิธีใส่ใน Render Environment Variables

---

**พร้อม deploy แล้วครับ!** 🚀

มีปัญหาตรงไหนถามได้เลยครับ
