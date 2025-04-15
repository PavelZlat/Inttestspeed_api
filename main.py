from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
from datetime import datetime

app = FastAPI()

# Модель данных для сохранения результатов
class SpeedTestResult(BaseModel):
    user_id: str
    download_speed: float
    upload_speed: float
    ping: float

# Функция для создания базы данных и таблицы, если они не существуют
def init_db():
    conn = sqlite3.connect("speedtest.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT,
        download_speed REAL,
        upload_speed REAL,
        ping REAL,
        timestamp TEXT
    )
    """)
    conn.commit()
    conn.close()

# Этот код будет выполняться при старте приложения
@app.on_event("startup")
def on_startup():
    init_db()  # Инициализация базы данных и таблицы при старте

# Корневой endpoint для проверки состояния сервера
@app.get("/")
def root():
    return {"message": "FastAPI Speedtest API is running ✅"}

# Endpoint для добавления результата теста
@app.post("/results/")
def add_result(result: SpeedTestResult):
    conn = sqlite3.connect("speedtest.db")
    cursor = conn.cursor()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Форматируем дату перед вставкой
    cursor.execute("INSERT INTO results (user_id, download_speed, upload_speed, ping, timestamp) VALUES (?, ?, ?, ?, ?)",
                   (result.user_id, result.download_speed, result.upload_speed, result.ping, timestamp))
    conn.commit()
    conn.close()
    return {"message": "Результат сохранён ✅"}

# Endpoint для получения последних 5 замеров по user_id
@app.get("/results/{user_id}")
def get_results(user_id: str):
    conn = sqlite3.connect("speedtest.db")
    cursor = conn.cursor()
    cursor.execute("SELECT download_speed, upload_speed, ping, timestamp FROM results WHERE user_id=? ORDER BY timestamp DESC LIMIT 5", (user_id,))
    rows = cursor.fetchall()
    conn.close()
    
    # Форматируем timestamp для каждого результата
    results = [
        {
            "download_speed": row[0],
            "upload_speed": row[1],
            "ping": row[2],
            "timestamp": datetime.strptime(row[3], "%Y-%m-%d %H:%M:%S").strftime("%d.%m.%Y %H:%M")  # Форматируем дату
        }
        for row in rows
    ]
    return results