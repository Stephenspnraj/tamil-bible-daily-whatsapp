import requests
import pandas as pd
from datetime import date
import os

# === Environment Variables (from GitHub Secrets) ===
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
YOUR_WHATSAPP_NUMBER = os.getenv("YOUR_WHATSAPP_NUMBER")

CSV_FILE = "bible_reading_plan.csv"


def format_daily_message(date_str, ot_chapter, nt_chapter, ot_questions, nt_questions):
    """Format Tamil WhatsApp message"""
    message = f"""📅 *இன்றைய வேதாகம வாசிப்பு ({date_str})*

📜 *பழைய ஏற்பாடு:* {ot_chapter}
📜 *புதிய ஏற்பாடு:* {nt_chapter}

💭 *பழைய ஏற்பாடு கேள்விகள்:*
{ot_questions.strip()}

💭 *புதிய ஏற்பாடு கேள்விகள்:*
{nt_questions.strip()}

🙏 *உங்கள் பதிலை 1️⃣ 2️⃣ 3️⃣ என அனுப்புங்கள்!*"""
    return message


def get_today_plan():
    """Read today's row from CSV"""
    df = pd.read_csv(CSV_FILE, encoding="utf-8")
    today = date.today().strftime("%Y-%m-%d")

    # Date match (support both yyyy-mm-dd or dd/mm/yyyy)
    row = df.loc[
        (df["Date"] == today)
        | (df["Date"] == date.today().strftime("%d/%m/%Y"))
    ]

    if row.empty:
        return None

    row = row.iloc[0]

    ot_chapter = row["OT_Chapter"]
    nt_chapter = row["NT_Chapter"]
    questions = str(row.get("Questions", "")).split("||")

    ot_questions = "\n".join(
        [f"{i+1}️⃣ {q.strip()}" for i, q in enumerate(questions[0].split("|")) if q.strip()]
    )

    nt_questions = ""
    if len(questions) > 1:
        nt_questions = "\n".join(
            [f"{i+1}️⃣ {q.strip()}" for i, q in enumerate(questions[1].split("|")) if q.strip()]
        )

    return format_daily_message(
        date.today().strftime("%d %B %Y"), ot_chapter, nt_chapter, ot_questions, nt_questions
    )


def send_whatsapp_message(message):
    """Send WhatsApp message via Meta Cloud API"""
    url = f"https://graph.facebook.com/v17.0/{PHONE_NUMBER_ID}/messages"
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}", "Content-Type": "application/json"}
    payload = {
        "messaging_product": "whatsapp",
        "to": YOUR_WHATSAPP_NUMBER,
        "type": "text",
        "text": {"body": message},
    }

    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        print("✅ Message sent successfully!")
    else:
        print("❌ Error:", response.text)


if __name__ == "__main__":
    message = get_today_plan()
    if message:
        send_whatsapp_message(message)
    else:
        print("⚠️ No plan found for today.")
