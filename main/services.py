import sqlite3
from datetime import datetime, timedelta
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

class AIService:
    def __init__(self):
        API_KEY = os.getenv("OPEN_API_KEY")
        MAX_MESSAGES_PER_SESSION = 10

    # ===== OpenAI клиент =====
        client = OpenAI(api_key=API_KEY)

    # ===== SQLite база данных =====
    conn = sqlite3.connect("chatbot_data.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT,
        session_id INTEGER,
        date TEXT,
        mood TEXT,
        reason TEXT,
        language TEXT,
        bot_response TEXT
    )
    """)
    conn.commit()

    # ===== Сессии пользователей =====
    sessions = {}

    # ===== System Prompt =====
    SYSTEM_PROMPT = """
    You are an emotional support assistant.
    User writes about mood, feelings, and activities.
    Your tasks:
    1. Summarize the user's mood (good, neutral, bad, etc.)
    2. Provide advice in the same language the user wrote (Kazakh, Russian, or English)
    3. Suggest a small action or challenge to improve their mood
    4. Always give a complete answer
    5. Include a short "Mood: ..., Reason: ..." for database storage
    """

    # ===== Функции =====
    def get_session(user_id):
        if user_id not in sessions:
            sessions[user_id] = {"messages": [], "session_id": 1}
        elif len(sessions[user_id]["messages"]) >= MAX_MESSAGES_PER_SESSION:
            sessions[user_id]["session_id"] += 1
            sessions[user_id]["messages"] = []
        return sessions[user_id]

    def save_message(user_id, session_id, date, mood, reason, language, bot_response):
        cursor.execute("""
            INSERT INTO messages (user_id, session_id, date, mood, reason, language, bot_response)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (user_id, session_id, date, mood, reason, language, bot_response))
        conn.commit()

    def generate_response(user_id, user_text):
        session = get_session(user_id)
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        for msg in session["messages"]:
            messages.append({"role": "user", "content": msg})
        messages.append({"role": "user", "content": user_text})

        response = client.chat.completions.create(
            model="gpt-5-chat-latest",  # GPT-5 для чата
            messages=messages,
            max_completion_tokens=400
        )
        bot_reply = response.choices[0].message.content
        session["messages"].append(user_text)
        return bot_reply

    def extract_mood_and_reason(bot_reply):
        mood, reason, language = "neutral", "", "unknown"
        lines = bot_reply.splitlines()
        for line in lines:
            low = line.lower()
            if low.startswith("mood:"):
                mood = low.replace("mood:", "").strip()
            elif low.startswith("reason:"):
                reason = low.replace("reason:", "").strip()
            elif low.startswith("language:"):
                language = low.replace("language:", "").strip()
        return mood, reason, language

    def request_report(user_id, days=30):
        since_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
        cursor.execute("""
            SELECT date, mood, reason, language, bot_response
            FROM messages
            WHERE user_id = ? AND date >= ?
            ORDER BY date ASC
        """, (user_id, since_date))
        return cursor.fetchall()

    def chat():
        user_id = input("Enter your user ID: ")
        while True:
            user_text = input("You: ")
            if user_text.lower() in ["exit", "quit"]:
                break
            if "report" in user_text.lower():
                report = request_report(user_id)
                for row in report:
                    print(f"Date: {row[0]}, Mood: {row[1]}, Reason: {row[2]}, Language: {row[3]}, Bot: {row[4]}")
                continue
            bot_reply = generate_response(user_id, user_text)
            mood, reason, language = extract_mood_and_reason(bot_reply)
            save_message(
                user_id,
                sessions[user_id]["session_id"],
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                mood, reason, language,
                bot_reply
            )
            print("Bot:", bot_reply)

if __name__ == "__main__":
    chat()
