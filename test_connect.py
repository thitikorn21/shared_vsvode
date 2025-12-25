import os
from databricks import sql
import time
from dotenv import load_dotenv # 1. ต้อง import
load_dotenv()               # 2. โหลด .env

# --- ใส่ค่า Config ของคุณ ---
SERVER_HOSTNAME = os.getenv("DATABRICKS_SERVER_HOSTNAME")
HTTP_PATH = os.getenv("DATABRICKS_HTTP_PATH")
ACCESS_TOKEN = os.getenv("DATABRICKS_TOKEN")

print("--- เริ่มทดสอบการเชื่อมต่อ ---")
start_time = time.time()

try:
    print(f"1. กำลังเชื่อมต่อ... (เวลาผ่านไป: {time.time() - start_time:.1f} วินาที)")
    connection = sql.connect(
        server_hostname=SERVER_HOSTNAME,
        http_path=HTTP_PATH,
        access_token=ACCESS_TOKEN
    )
    
    print(f"2. เชื่อมต่อสำเร็จ! (ใช้เวลา: {time.time() - start_time:.1f} วินาที)")
    print("3. กำลังลองดึงข้อมูล 1 แถว...")
    
    cursor = connection.cursor()
    cursor.execute("SELECT 1") # Query ง่ายๆ แค่เช็คว่าคุยกันรู้เรื่องไหม
    result = cursor.fetchone()
    
    print(f"--- ✅ สำเร็จ! ผลลัพธ์คือ: {result} ---")
    
    cursor.close()
    connection.close()

except Exception as e:
    print(f"\n--- ❌ ล้มเหลว! เกิด Error: ---\n{e}")