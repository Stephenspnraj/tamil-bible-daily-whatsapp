import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests
import os
from datetime import datetime

# -------------------------------
# Google Sheet Setup
# -------------------------------
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name("service_account.json", SCOPE)
client = gspread.authorize(creds)

sheet = client.open_by_key("12ak_BlCZpTOZWWGX0wy_rbCcMLaJaLc9JdDkBo9nzQw")

birthday_sheet = sheet.worksheet("Birthdays")
wedding_sheet = sheet.worksheet("Weddings")

birthday_rows = birthday_sheet.get_all_records()
wedding_rows = wedding_sheet.get_all_records()

# -------------------------------
# WhatsApp Cloud API
# -------------------------------
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")       # From GitHub Secrets
PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_ID")   # From GitHub Secrets

# Your WhatsApp number (the one you want to receive messages)
MY_NUMBER = os.getenv("MY_WHATSAPP_NUMBER")        # Example: "919876543210"

API_URL = f"https://graph.facebook.com/v17.0/{PHONE_NUMBER_ID}/messages"

today = datetime.today().strftime("%m-%d")


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
# Build message content
# ------------------------------

def parse_date(date):
    for fmt in ("%Y-%m-%d", "%d/%m/%Y"):
        try:
            return datetime.strptime(date, fmt)
        except:
            continue
    return None

birthday_list = []
wedding_list = []

# Birthdays
for row in birthday_rows:
    name = row["Name"]
    date = str(row["Date"])
    dt = parse_date(date)
    if dt and dt.strftime("%m-%d") == today:
        birthday_list.append(name)  # ✅ properly indented

# Weddings
for row in wedding_rows:
    name = row["Name"]
    date = str(row["Date"])
    dt = parse_date(date)
    if dt and dt.strftime("%m-%d") == today:
        wedding_list.append(name)  # ✅ properly indented


# If nothing today → exit silently
if not birthday_list and not wedding_list:
    exit()


# -------------------------------
# Create a single WhatsApp message
# -------------------------------
message = "📅 *Today's Celebrations*\n\n"

if birthday_list:
    message += "🎂 *Birthdays:*\n"
    for b in birthday_list:
        message += f"• {b}\n"
    message += "\n"

if wedding_list:
    message += "💍 *Wedding Anniversaries:*\n"
    for w in wedding_list:
        message += f"• {w}\n"

message += "\nForward this message to the group. 🚀"

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

print("Today:", today)
print("Birthday rows:", birthday_rows)
print("Wedding rows:", wedding_rows)




# -------------------------------
# Send to YOUR WhatsApp
# -------------------------------
send_whatsapp(MY_NUMBER, message)
