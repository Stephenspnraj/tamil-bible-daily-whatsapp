import csv
import requests
from datetime import datetime, timedelta
import time
import pytz

# ==== CONFIG ====
ACCESS_TOKEN = "YOUR_ACCESS_TOKEN"
PHONE_NUMBER_ID = "YOUR_PHONE_NUMBER_ID"
GROUP_ID = "YOUR_GROUP_ID_OR_PHONE"  # e.g. "1203630xxxxxx@g.us"
CSV_FILE = "bible_reading_plan.csv"
SEND_HOUR = 6  # 6 AM IST

# ==== HELPERS ====
def send_whatsapp_message(to, message):
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
        print("❌ Error:", response.text)

# ==== READ CSV ====
def read_today_data():
    today = datetime.now(pytz.timezone("Asia/Kolkata")).strftime("%Y-%m-%d")
    with open(CSV_FILE, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["Date"] == today:
                return row
    return None

# ==== MAIN ====
def main():
    data = read_today_data()
    if not data:
        print("No data found for today in CSV.")
        return

    # ---- Prepare messages ----
    date_str = datetime.now(pytz.timezone("Asia/Kolkata")).strftime("%-d %B %Y")
    msg1 = (
        f"📅 Daily message:\n"
        f"📖 இன்றைய வேதாகம வாசிப்பு ({date_str})\n\n"
        f"📜 பழைய ஏற்பாடு: {data['OT_Chapter']}\n"
        f"📜 புதிய ஏற்பாடு: {data['NT_Chapter']}\n\n"
        f"💭 கேள்விகள்:\n{data['Questions']}"
    )

    msg2 = f"📜 இன்றைய பதில்கள்:\n{data['Answers']}"

    # ---- Send message 1 ----
    send_whatsapp_message(GROUP_ID, msg1)

    # ---- Wait 10 minutes ----
    print("⏳ Waiting 10 minutes before sending answers...")
    time.sleep(600)

    # ---- Send message 2 ----
    send_whatsapp_message(GROUP_ID, msg2)

if __name__ == "__main__":
    main()
