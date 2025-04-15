from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
from datetime import datetime

app = FastAPI()

# модель запроса для сохранения результата
class SpeedTestResult(BaseModel):
    user_id: str
    download_speed: float
    upload_speed: float
    ping: float

# endpoint для сохранения результата
@app.post("/results/")
def add_result(result: SpeedTestResult):
    conn = sqlite3.connect("speedtest.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO results (user_id, download_speed, upload_speed, ping, timestamp) VALUES (?, ?, ?, ?, ?)",
                   (result.user_id, result.download_speed, result.upload_speed, result.ping, datetime.now()))
    conn.commit()
    conn.close()
    return {"message": "Результат сохранён ✅"}

# endpoint для получения последних 5 замеров пользователя
@app.get("/results/{user_id}")
def get_results(user_id: str):
    conn = sqlite3.connect("speedtest.db")
    cursor = conn.cursor()
    cursor.execute("SELECT download_speed, upload_speed, ping, timestamp FROM results WHERE user_id=? ORDER BY timestamp DESC LIMIT 5", (user_id,))
    rows = cursor.fetchall()
    conn.close()
    results = [
        {
            "download_speed": row[0],
            "upload_speed": row[1],
            "ping": row[2],
            "timestamp": row[3]
        }
        for row in rows
    ]
    return results