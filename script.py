import csv
import requests
from datetime import datetime
import time
import pytz
import os

# ==== CONFIG ====
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
YOUR_WHATSAPP_NUMBER = os.getenv("YOUR_WHATSAPP_NUMBER")
CSV_FILE = "bible_reading_plan.csv"

# ==== HELPERS ====
def send_whatsapp_message(to, message):
    """Send message via WhatsApp Cloud API."""
    url = f"https://graph.facebook.com/v20.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"preview_url": False, "body": message}
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        print("✅ Message sent successfully!")
    else:
        print("❌ Error sending message:", response.text)

# ==== READ CSV ====
def read_today_data():
    today = datetime.now(pytz.timezone("Asia/Kolkata")).strftime("%Y-%m-%d")
    with open(CSV_FILE, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["Date"].strip() == today:
                return row
    return None

# ==== MAIN ====
def main():
    data = read_today_data()
    if not data:
        print("⚠️ No data found for today in CSV.")
        return

    date_str = datetime.now(pytz.timezone("Asia/Kolkata")).strftime("%-d %B %Y")

    msg1 = (
        f"📖 ஒரு வருட  வேதாகம வாசிப்பு   திட்டம்:\n"
        f"📖 இன்றைய வேதாகம வாசிப்பு ({date_str})\n\n"
        f"📜 பழைய ஏற்பாடு: {data['OT_Chapter']}\n"
        f"📜 புதிய ஏற்பாடு: {data['NT_Chapter']}\n\n"
    )

    msg2 = f"💭 கேள்விகள்:\n{data['Questions']}"

    msg3 = f"📜 இன்றைய பதில்கள்:\n{data['Answers']}"

    # ---- Send message 1 ----
    send_whatsapp_message(YOUR_WHATSAPP_NUMBER, msg1)

    # ---- Wait 10 minutes ----
    print("⏳ Waiting 5 seconds before sending answers...")
    time.sleep(5)

    # ---- Send message 2 ----
    send_whatsapp_message(YOUR_WHATSAPP_NUMBER, msg2)
    send_whatsapp_message(YOUR_WHATSAPP_NUMBER, msg3)

if __name__ == "__main__":
    main()
