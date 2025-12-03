from main.models import Message, ChatSession
from datetime import datetime, timedelta
from openai import OpenAI
from dotenv import load_dotenv
import os

from openai.resources.beta.threads import Messages

from users.models import User

load_dotenv()

class AIService:
    def __init__(self):
        API_KEY = os.getenv("OPEN_API_KEY")
        self.MAX_MESSAGES_PER_SESSION = 10
        self.client = OpenAI(api_key=API_KEY)
        self.sessions = {}


        self.SYSTEM_PROMPT = SYSTEM_PROMPT = """
        You are an emotional support assistant.
        User writes about mood, feelings, and activities.
        Your tasks:
        1. Summarize the user's mood (good, neutral, bad, etc.)
        2. Provide advice in the same language the user wrote (Kazakh, Russian, or English)
        3. Suggest a small action or challenge to improve their mood
        4. Always give a complete answer
        5. Include a short "Mood: ..., Reason: ..." for database storage
        
        When user asks to create a schedule for today, you must ALWAYS return a JSON array of tasks.
        Each task is an object with:
        - description (string)
        - time (HH:MM)
        - status (todo, in_progress, completed)
        
        Example output:
        {
          "type": "schedule",
          "tasks": [
            {"description": "Завтрак", "time": "08:00", "status": "todo"},
            {"description": "Прогулка", "time": "09:30", "status": "todo"}
          ]
        }
        
        Do not return any text except this JSON when generating a schedule.        
        """

    # ===== Функции =====
    def get_session(self, user_id):
        if user_id not in self.sessions:
            self.sessions[user_id] = {"messages": [], "session_id": 1}
        elif len(self.sessions[user_id]["messages"]) >= self.MAX_MESSAGES_PER_SESSION:
            self.sessions[user_id]["session_id"] += 1
            self.sessions[user_id]["messages"] = []
        return self.sessions[user_id]

    def save_message(self, user, session: ChatSession, user_message, date, mood, reason, language, bot_response):
        new_message = Message.objects.create(user=user, user_message=user_message, session=session, mood=mood, reason=reason, language=language, bot_response=bot_response)
        return new_message
    def generate_response(self, user_id, user_text):
        session = self.get_session(user_id)
        messages = [{"role": "system", "content": self.SYSTEM_PROMPT}]
        for msg in session["messages"]:
            messages.append({"role": "user", "content": msg})
        messages.append({"role": "user", "content": user_text})

        response = self.client.chat.completions.create(
            model="gpt-5-chat-latest",  # GPT-5 для чата
            messages=messages,
            max_completion_tokens=400
        )
        bot_reply = response.choices[0].message.content
        session["messages"].append(user_text)
        return bot_reply

    def extract_mood_and_reason(self, bot_reply):
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

    def request_report(self, user_id, days=30):
        since_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
        report = Message.objects.filter(user_id=user_id, date=since_date).all()
        return report

    def extract_user_text(self, bot_reply: str) -> str:
        lines = bot_reply.splitlines()
        user_lines = []
        skip_prefixes = ["**Mood:**", "**Reason:**", "**Mood: neutral, Reason:"]  # всё служебное

        for line in lines:
            if any(line.startswith(prefix) for prefix in skip_prefixes):
                continue
            user_lines.append(line)

        return "\n".join([l for l in user_lines if l.strip()])
    def chat(self, user_id):

        while True:
            user_text = input("You: ")
            if user_text.lower() in ["exit", "quit"]:
                break
            if "report" in user_text.lower():
                report = self.request_report(user_id)
                for row in report:
                    print(f"Date: {row[0]}, Mood: {row[1]}, Reason: {row[2]}, Language: {row[3]}, Bot: {row[4]}")
                continue
            bot_reply = self.generate_response(user_id, user_text)
            mood, reason, language = self.extract_mood_and_reason(bot_reply)
            self.save_message(
                User.objects.get(id=user_id),
                self.sessions[user_id]["session_id"],
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                mood, reason, language,
                bot_reply
            )

            print("Bot:", bot_reply)

