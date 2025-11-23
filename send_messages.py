import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import requests
import os
import json

# -------------------------------
# Environment variables from GitHub
# -------------------------------
WHATSAPP_TOKEN = os.environ["ACCESS_TOKEN"]
WHATSAPP_PHONE_ID = os.environ["PHONE_NUMBER_ID"]
MY_NUMBER = os.environ["YOUR_WHATSAPP_NUMBER"]
GOOGLE_CREDS_JSON = os.environ["GOOGLE_CREDENTIALS"]

API_URL = f"https://graph.facebook.com/v17.0/{WHATSAPP_PHONE_ID}/messages"

# -------------------------------
# Google Sheets setup
# -------------------------------
SCOPE = ["https://www.googleapis.com/auth/spreadsheets"]

# Write the JSON secret to a file
service_account_file = "service_account.json"
with open(service_account_file, "w") as f:
    f.write(GOOGLE_CREDS_JSON)

creds = ServiceAccountCredentials.from_json_keyfile_name(service_account_file, SCOPE)
client = gspread.authorize(creds)

# Replace with your Google Sheet ID
SHEET_ID = "12ak_BlCZpTOZWWGX0wy_rbCcMLaJaLc9JdDkBo9nzQw"
sheet = client.open_by_key(SHEET_ID)

# Load worksheets
birthday_sheet = sheet.worksheet("Birthday")
wedding_sheet = sheet.worksheet("Weddings")

birthday_rows = birthday_sheet.get_all_records()
wedding_rows = wedding_sheet.get_all_records()

today = datetime.today().strftime("%m-%d")
print("Today:", today)

# -------------------------------
# Date parsing function
# -------------------------------
def parse_date(date):
    for fmt in ("%Y-%m-%d", "%d/%m/%Y"):
        try:
            return datetime.strptime(date, fmt)
        except:
            continue
    return None

# -------------------------------
# Build lists
# -------------------------------
birthday_list = []
wedding_list = []

# Birthdays
for row in birthday_rows:
    name = row.get("Name")
    date = str(row.get("Date"))
    dt = parse_date(date)
    if dt and dt.strftime("%m-%d") == today:
        birthday_list.append(name)

# Weddings
for row in wedding_rows:
    name = row.get("Name")
    date = str(row.get("Date"))
    dt = parse_date(date)
    if dt and dt.strftime("%m-%d") == today:
        wedding_list.append(name)

print("Birthdays today:", birthday_list)
print("Weddings today:", wedding_list)

# -------------------------------
# Build message
# -------------------------------
message = ""
if birthday_list:
    message += "🎂 Birthdays:\n" + "\n".join(f"• {b}" for b in birthday_list) + "\n\n"
if wedding_list:
    message += "💍 Weddings:\n" + "\n".join(f"• {w}" for w in wedding_list)

# -------------------------------
# WhatsApp sending
# -------------------------------
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
    response = requests.post(API_URL, json=body, headers=headers)
    print("WhatsApp API response:", response.status_code, response.text)

if message:
    print("Sending WhatsApp message:\n", message)
    send_whatsapp(MY_NUMBER, message)
else:
    print("No birthdays or weddings today.")
