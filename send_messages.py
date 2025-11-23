import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests
import os
from datetime import datetime

# ---- Google Sheet Setup ----
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]


creds = ServiceAccountCredentials.from_json_keyfile_name("service_account.json", SCOPE)
client = gspread.authorize(creds)
sheet = client.open_by_key("12ak_BlCZpTOZWWGX0wy_rbCcMLaJaLc9JdDkBo9nzQw")

# Load sheets
birthday_sheet = client.open("CCA Member's details").worksheet("Birthday")
wedding_sheet = client.open("CCA Member's details").worksheet("Weddings")

birthday_rows = birthday_sheet.get_all_records()
wedding_rows = wedding_sheet.get_all_records()

# ---- WhatsApp Cloud API ----
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_ID")
API_URL = f"https://graph.facebook.com/v17.0/{PHONE_NUMBER_ID}/messages"

today = datetime.today().strftime("%m-%d")  # format MM-DD

def send_whatsapp(to, text):
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    body = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": text}
    }
    requests.post(API_URL, json=body, headers=headers)


# -------------------------------
# 🎂 Handle Birthday Messages
# -------------------------------
for i, row in enumerate(birthday_rows, start=2):  # start=2 -> skips header
    name = row["Name"]
    date = row["Date"]   # format YYYY-MM-DD
    phone = row.get("Phone", "")  # if you later add phone column

    # Validate date exists
    if not date:
        continue

    # If the date matches today
    if datetime.strptime(date, "%Y-%m-%d").strftime("%m-%d") == today:

        message = f"🎉 Happy Birthday, {name}! Wishing you a wonderful year ahead!"

        send_whatsapp(phone, message)

        # Update sheet (optional tracking column)
        birthday_sheet.update_cell(i, 3, "SENT")  # writes into column C


# -------------------------------
# 💍 Handle Wedding Anniversary Messages
# -------------------------------
for i, row in enumerate(wedding_rows, start=2):
    name = row["Name"]
    date = row["Date"]
    phone = row.get("Phone", "")

    if not date:
        continue

    if datetime.strptime(date, "%Y-%m-%d").strftime("%m-%d") == today:

        message = f"💍 Happy Wedding Anniversary, {name}! Many more years of happiness to you!"

        send_whatsapp(phone, message)

        # Update sheet
        wedding_sheet.update_cell(i, 3, "SENT")
