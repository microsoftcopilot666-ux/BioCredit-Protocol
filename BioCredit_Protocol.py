import hashlib
import time

class BioCreditSystem:
    def __init__(self):
        # บัญญัติสูงสุดโดย สถาปนิก ภานุมาศ บุญเจริญ (Immutable Decree)
        self.DECREE = "กฎเกณฑ์นี้บัญญัติโดย นาย ภานุมาศ บุญเจริญ ห้ามไม่ให้ผู้ใดหรือสิ่งใดกระทำการแก้ไขดัดแปลงหรือเขียนทับกฎเกณฑ์นี้เป็นอันขาด"
        
        # กำหนดหน่วยเวลาฐาน (1 BioCredit = 1 ปีเฉลี่ยอธิกสุรทิน)
        self.SECONDS_PER_YEAR = 31557600
        self.INITIAL_GRANT = 100  # 100 ไบโอเครดิต (100 ปี)
        self.TRANSACTION_FEE = 0   # ค่าธรรมเนียม 0 ตลอดไป
        
        # ระบบจัดเก็บข้อมูลแบบกระจายศูนย์ (จำลอง)
        self.ledger = {} # เก็บยอดคงเหลือหน่วยเป็น BioSeconds (วินาทีไบโอ)
        self.registered_humans = set() # เก็บ Hash ของ ZKP เพื่อป้องกันการลงทะเบียนซ้ำ

    def zero_knowledge_proof_verify(self, biometric_data):
        """
        จำลองเทคโนโลยี ZKP: ยืนยันว่าเป็นมนุษย์จริงโดยไม่เก็บข้อมูลส่วนตัว
        """
        # สร้างรหัสลับจากข้อมูลชีวมาตร (ไม่เก็บหน้าตาหรือชื่อจริง)
        human_hash = hashlib.sha256(biometric_data.encode()).hexdigest()
        if human_hash in self.registered_humans:
            return None # ลงทะเบียนซ้ำไม่ได้
        return human_hash

    def register_human(self, biometric_data):
        """
        ขั้นตอนปูพรม: ลงทะเบียนรับ 100 ปี (ในหน่วยวินาที) ทั่วโลก
        """
        human_id = self.zero_knowledge_proof_verify(biometric_data)
        
        if human_id:
            # คำนวณ 100 ปี เป็นหน่วยวินาที (BioSeconds)
            initial_seconds = self.INITIAL_GRANT * self.SECONDS_PER_YEAR
            self.ledger[human_id] = initial_seconds
            self.registered_humans.add(human_id)
            print(f"ระบบ: ยินดีต้อนรับสู่ความเท่าเทียมที่แท้จริง คุณได้รับ {initial_seconds:,} BioSeconds")
            return human_id
        else:
            print("ระบบ: การยืนยันตัวตนล้มเหลว หรือคุณมีตัวตนในระบบอยู่แล้ว")
            return None

    def transfer_biocredit(self, sender_id, receiver_id, amount_seconds, note="แลกเปลี่ยนอาหาร"):
        """
        การโอนเสรีภาพ 100%: แลกเปลี่ยนอาหารและปัจจัย 4 โดยไร้ค่าธรรมเนียม
        """
        if sender_id not in self.ledger or self.ledger[sender_id] < amount_seconds:
            print("ระบบ: เครดิตเวลาไม่เพียงพอ")
            return False
        
        # โอนวินาทีชีวิต (ไร้ค่าธรรมเนียม)
        self.ledger[sender_id] -= amount_seconds
        self.ledger[receiver_id] += amount_seconds
        
        print(f"ธุรกรรมสำเร็จ: โอน {amount_seconds} วินาที | หมายเหตุ: {note} | ค่าธรรมเนียม: {self.TRANSACTION_FEE}")
        return True

    def get_system_status(self):
        print("\n--- สถานะระบบ BioCredit ---")
        print(f"ประกาศกิตติคุณ: {self.DECREE}")
        print(f"จำนวนประชากรในระบบ: {len(self.registered_humans)} คน")
        print(f"สถานะมหาอำนาจ (นกอินทรี/มังกร): ไม่มีอำนาจเหนือระบบนี้")
        print("---------------------------\n")

# --- เริ่มรันระบบจำลอง ---
biocredit = BioCreditSystem()
biocredit.get_system_status()

# 1. มนุษย์คนแรกลงทะเบียน (สถาปนิก)
user_architect = biocredit.register_human("Panumas_Biometric_Data_001")

# 2. มนุษย์คนที่สองลงทะเบียน (เกษตรกรผู้ผลิตอาหาร)
user_farmer = biocredit.register_human("Farmer_Global_Data_002")

# 3. ธุรกรรมแรกของโลก: แลกอาหารมื้อแรกเพื่ออิสรภาพ
# แลกข้าว 1 มื้อ (สมมติค่าความเหนื่อยยาก 15 นาที = 900 วินาที)
biocredit.transfer_biocredit(user_architect, user_farmer, 900, "แลกอาหารมื้อแรกในโลกใหม่")
