import requests
import pandas as pd
from datetime import date

# Environment variables from GitHub Actions secrets
import os
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
YOUR_WHATSAPP_NUMBER = os.getenv("YOUR_WHATSAPP_NUMBER")

CSV_FILE = "bible_reading_plan.csv"

def get_today_plan():
    df = pd.read_csv(CSV_FILE)
    today = date.today().strftime("%Y-%m-%d")
    row = df.loc[df['Date'] == today]
    if row.empty:
        return None
    row = row.iloc[0]
    message = f"""📖 *இன்றைய வேதாகம வாசிப்பு ({today})*:

📜 *பழைய ஏற்பாடு:* {row['OT_Chapter']}
📜 *புதிய ஏற்பாடு:* {row['NT_Chapter']}

💭 *கேள்விகள்:*
{row['Questions']}
"""
    return message

def send_whatsapp_message(message):
    url = f"https://graph.facebook.com/v17.0/{PHONE_NUMBER_ID}/messages"
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    payload = {
        "messaging_product": "whatsapp",
        "to": YOUR_WHATSAPP_NUMBER,
        "type": "text",
        "text": {"body": message}
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
