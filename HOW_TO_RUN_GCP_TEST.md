# 🚀 คู่มือการทดสอบ PLE บน GCP Spot VM (แบบประหยัดสุดขีด & ดับเครื่องอัตโนมัติ)

เอกสารนี้สรุปขั้นตอนการรันชุดทดสอบ **Physical-Engineering's Last Exam (PLE)** บน **Google Cloud Platform (GCP)** โดยจำลองสภาพแวดล้อมให้ตรงกับ **Stage 2** ของการแข่งขัน 100% และใช้ต้นทุนต่ำที่สุด (~1 - 4 บาท / ครั้ง)

---

## 📌 จุดเด่นของระบบนี้ (Cost-Optimized & Auto-Termination)
1. **จำลองสเปก Stage 2 เป๊ะๆ:** จำกัดทรัพยากรที่ **2 vCPUs, 4 GB RAM** และพื้นที่ชั่วคราว 1 GB
2. **ประหยัดค่าใช้จ่าย 60-90%:** ใช้เครื่อง **Spot VM (`e2-standard-2`)** อัตราค่าบริการเพียง ~0.50 บาท/ชม.
3. **ป้องกันค่าใช้จ่ายบานปลาย (Self-Terminating):**
   * ตั้งเวลาทำงานสูงสุดไม่เกิน **5 ชั่วโมง 50 นาที**
   * เมื่อรันเสร็จ (หรือติด Timeout/OOM) จะดูดผลลัพธ์และ Log ขึ้น **Google Cloud Storage (GCS)** ทันที
   * สั่ง **`DELETE` ตัวเองทิ้งจากระบบทันที** ไม่มีการเปิดเครื่องทิ้งไว้ และไม่เสียค่าเช่า Disk ค้างคา

---

## ⚡ วิธีสั่งรันจากเครื่องของคุณ (คำสั่งเดียว อัตโนมัติ 100%)

เปิด **PowerShell** บนเครื่องของคุณ แล้วรันคำสั่ง:

```powershell
# 1. เข้าสู่โฟลเดอร์โปรเจกต์
cd C:\Users\takon\OneDrive\Desktop\da\project-debim\debim-ple-harness

# 2. สั่งยิง Spot VM ขึ้นไปรันโจทย์
.\launch_spot_vm.ps1 -TaskName "engineers-estimate-check"
```

### 🤖 สิ่งที่ระบบจะทำให้คุณโดยอัตโนมัติ (End-to-End):
1. **สร้าง Spot VM บน GCP** สเปก 2 vCPU, 4GB RAM ใน Zone `us-central1-a`
2. **ดาวน์โหลดโจทย์อัตโนมัติ:** VM จะไปดึงชุดประเมินจาก `google-research/ple` และดาวน์โหลดไฟล์โจทย์ของข้อนั้น (CAD, drawings, specs) จาก Hugging Face ให้เองอัตโนมัติ
3. **รันประเมินและตรวจคะแนน:** รัน `eval/run.py` ควบคู่กับ Harness ตัวใหม่ (`google-antigravity` + `debim 1.3.0`)
4. **ส่งผลลัพธ์ขึ้น Cloud Storage:** ผลคะแนนและ Artifacts ใน `runs/` จะถูกอัปโหลดขึ้น `gs://lab-ai-972593-ple-results/`
5. **ลบตัวเองทิ้งทันที:** ป้องกันค่าใช้จ่ายค้างคา เสียเงินเพียงแค่หลักบาทเดียวตามเวลาที่รันจริง

---

## 🔍 วิธีติดตามผลและดู Log แบบ Real-time

### 1. ดูหน้าจอการทำงาน (Serial Port Console) จากเครื่องคุณ:
หลังจากรันสคริปต์ ระบบจะแจ้งชื่อ VM เช่น `ple-runner-1119-1249` คุณสามารถดู Log สดๆ ได้ด้วยคำสั่ง:
```powershell
gcloud compute instances get-serial-port-output <ชื่อ-VM> --zone=us-central1-a --follow
```
*(กด `Ctrl + C` เพื่อหยุดดูได้ตลอดเวลา โดยที่ VM ยังคงทำงานต่อตามปกติ)*

### 2. ดาวน์โหลดผลลัพธ์กลับมาดูที่เครื่องหลังจาก VM ทำงานเสร็จ:
เมื่อเครื่องรันเสร็จและลบตัวเองแล้ว ผลลัพธ์จะอยู่ใน Cloud Storage:
```powershell
# ดูรายการไฟล์ผลลัพธ์ใน Bucket
gcloud storage ls gs://lab-ai-972593-ple-results/test-mep-routing-01/

# ดาวน์โหลดโฟลเดอร์ output กลับลงมาที่เครื่อง
gcloud storage cp -r gs://lab-ai-972593-ple-results/test-mep-routing-01/output ./downloaded_results/
```

---

## 📁 โครงสร้างไฟล์ที่เกี่ยวข้องในโปรเจกต์

| ไฟล์ | หน้าที่ |
| :--- | :--- |
| **`launch_spot_vm.ps1`** | สคริปต์ PowerShell สำหรับยิงคำสั่งสร้าง Spot VM จากเครื่องเรา |
| **`scripts/gcp_spot_startup.sh`** | Startup script ในเครื่อง VM ที่คอยคุมคอนเทนเนอร์ Stage 2, ซิงค์ไฟล์ขึ้น GCS และสั่งลบเครื่อง |
| **`serve.py`** | โค้ดหลักที่ปรับปรุงใหม่ รองรับ `google-antigravity` Python SDK (In-Memory) และ `debim 1.3.0` |
| **`requirements.txt`** | ระบุแพ็กเกจ `google-antigravity==0.1.23` และ `debim>=1.3.0` |
| **`.env`** | บันทึก Gemini API Key สำหรับโปรเจกต์นี้ *(ถูกละเว้นใน `.gitignore` ปลอดภัยไม่ขึ้น Git)* |
| **`HOW_TO_RUN_GCP_TEST.md`** | ไฟล์คู่มือนี้ |
