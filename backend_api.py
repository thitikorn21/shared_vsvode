import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from databricks import sql
from pydantic import BaseModel
import uvicorn
from dotenv import load_dotenv # 1. ต้อง import
load_dotenv()               # 2. โหลด .env


app = FastAPI(title="Broadcast Data Platform API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Configuration (ใส่ค่าจริงของคุณที่นี่) ---
DATABRICKS_SERVER_HOSTNAME = os.getenv("DATABRICKS_SERVER_HOSTNAME")
DATABRICKS_HTTP_PATH = os.getenv("DATABRICKS_HTTP_PATH")
DATABRICKS_TOKEN = os.getenv("DATABRICKS_TOKEN")

def get_db_connection():
    return sql.connect(
        server_hostname=DATABRICKS_SERVER_HOSTNAME,
        http_path=DATABRICKS_HTTP_PATH,
        access_token=DATABRICKS_TOKEN
    )

# --- API 1: Daily Stats ---
@app.get("/api/stats/daily")
def get_daily_stats():
    print("1. [Daily Stats] Request received...")
    # ดึงเฉพาะ column ที่จำเป็น (ไม่เอา updated_at)
    query = """
    SELECT DISTINCT
        stat_date, stat_time, campaign_id, campaign_name, segment_name, 
        sent_count, read_count, click_count, estimated_cost 
    FROM main.project_l.campaign_daily_stats 
    ORDER BY stat_date DESC, stat_time DESC LIMIT 50
    """
    try:
        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
                
                data = []
                for row in result:
                    # --- Logic แก้ไขวันที่ซ้อนกัน ---
                    date_str = str(row.stat_date) # วันที่จริงจาก stat_date (เช่น 2025-11-21)
                    time_str = ""

                    if row.stat_time:
                        # stat_time เป็น Timestamp มันจะมีวันที่ติดมาด้วย (เช่น 2025-12-25 07:07:00)
                        # เราต้องตัดเอาแค่ "เวลา" ด้านหลัง
                        t_full = str(row.stat_time) 
                        if " " in t_full:
                            # แยกด้วยช่องว่าง แล้วเอาส่วนหลัง (เวลา)
                            time_only = t_full.split(" ")[1] 
                            # ตัดเศษวินาที (.000) หรือ timezone (+00:00) ออกถ้ามี
                            time_str = time_only.split(".")[0].split("+")[0]
                        else:
                            time_str = t_full

                    # รวมร่าง: วันที่จริง + เวลาที่ตัดมาแล้ว
                    date_display = f"{date_str} {time_str}".strip()

                    data.append({
                        "id": row.campaign_id,
                        "date": date_display,              # แสดงผล: 2025-11-21 07:07:00
                        "campaign": row.campaign_name,
                        "segment": row.segment_name,
                        "sent": row.sent_count,
                        "read": row.read_count,
                        "click": row.click_count,
                        "cost": float(row.estimated_cost or 0)
                    })
                return data
    except Exception as e:
        print(f"!!! ERROR [Daily] !!!: {e}")
        return []

# --- เพิ่ม API สำหรับดึงข้อมูล Flex Message ---
# --- แก้ไข API สำหรับดึงข้อมูล Flex Message ---
@app.get("/api/stats/flex")
def get_flex_stats():
    print("1. [Flex Stats] Request received...")
    query = """
    SELECT flex_name, flex_type, broadcast_count, total_sent, total_read, total_click 
    FROM main.project_l.flex_message_performance
    """
    try:
        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
                
                data = []
                for row in result:
                    # --- FIX: แปลง NULL เป็น 0 ให้หมดกันหน้าเว็บพัง ---
                    b_count = row.broadcast_count if row.broadcast_count else 0
                    sent = row.total_sent if row.total_sent else 0
                    read = row.total_read if row.total_read else 0
                    click = row.total_click if row.total_click else 0
                    
                    # คำนวณ CTR (Click / Read) * 100
                    ctr = (click / read * 100) if read > 0 else 0

                    data.append({
                        "name": row.flex_name,
                        "type": row.flex_type,
                        "broadcast_count": b_count, # ส่งค่าที่แก้เป็น 0 แล้ว
                        "total_sent": sent,
                        "total_read": read,        # ส่งค่าที่แก้เป็น 0 แล้ว
                        "total_click": click,
                        "ctr": ctr
                    })
                return data
    except Exception as e:
        print(f"!!! ERROR [Flex Stats] !!!: {e}")
        return []

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)