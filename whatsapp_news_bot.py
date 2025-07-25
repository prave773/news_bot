import requests
import os
from twilio.rest import Client

NEWSDATA_API_KEY = os.environ["NEWSDATA_API_KEY"]
TWILIO_SID = os.environ["TWILIO_SID"]
TWILIO_AUTH_TOKEN = os.environ["TWILIO_AUTH_TOKEN"]
FROM_WHATSAPP_NUMBER = os.environ["FROM_WHATSAPP_NUMBER"]
TO_WHATSAPP_NUMBER = os.environ["TO_WHATSAPP_NUMBER"]

client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

def get_latest_news():
    url = f"https://newsapi.org/v2/everything?q=India&language=en&sortBy=publishedAt&apiKey={NEWSDATA_API_KEY}"
    response = requests.get(url)
    data = response.json()

    if data.get("status") == "ok" and data.get("articles"):
        messages = []
        for article in data["articles"][:3]:
            title = article["title"]
            summary = article.get("description", "No summary available.")
            source = article.get("source", {}).get("name", "Unknown")
            pub_date = article.get("publishedAt", "Unknown")
            link = article.get("url", "#")
            messages.append(f"🗞️ *{title}*\n📍{source} | 🕒 {pub_date}\n🔗 {link}")
        return "\n\n".join(messages)
    return "⚠️ No news found."

def send_whatsapp_message(message):
    client.messages.create(
        from_=FROM_WHATSAPP_NUMBER,
        body=message,
        to=TO_WHATSAPP_NUMBER
    )

news = get_latest_news()
send_whatsapp_message(news)
