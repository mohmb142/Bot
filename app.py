import os
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "").strip()
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "").strip()

def send_telegram(text):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        raise RuntimeError("TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID are required")
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    r = requests.post(url, json={"chat_id": TELEGRAM_CHAT_ID, "text": text, "parse_mode": "HTML", "disable_web_page_preview": True}, timeout=5)
    r.raise_for_status()

def format_signal(data):
    side = data.get("side", "UNKNOWN")
    symbol = data.get("symbol", "UNKNOWN")
    timeframe = data.get("timeframe", "?")
    price = data.get("price", "?")
    event = data.get("event", "signal")
    if event == "signal":
        icon, title, status = ("🟢" if side == "BUY" else "🔴"), "إشارة جديدة", "⏳ بانتظار إغلاق شمعة الإشارة"
    elif event == "confirmed":
        icon, title, status = ("🟢" if side == "BUY" else "🔴"), "تم تأكيد الإشارة", "🔒 شمعة الإشارة أغلقت والإشارة ثابتة"
    elif event == "cancelled":
        icon, title, status = "⚠️", "إلغاء الإشارة", "الإشارة لم تبقَ موجودة عند إغلاق الشمعة"
    else:
        icon, title, status = "📩", "TradingView", ""
    return f"<b>{icon} {title}</b>\n\n📊 <b>{symbol}</b>\n📌 الاتجاه: <b>{side}</b>\n⏱ الفريم: <b>{timeframe}</b>\n💰 السعر: <b>{price}</b>\n\n{status}"

@app.get("/")
def health():
    return jsonify({"ok": True, "service": "TradingView Telegram Bot"})

@app.post("/webhook/<secret>")
def webhook(secret):
    if WEBHOOK_SECRET and secret != WEBHOOK_SECRET:
        return jsonify({"ok": False, "error": "unauthorized"}), 401
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"ok": False, "error": "JSON body required"}), 400
    try:
        send_telegram(format_signal(data))
        return jsonify({"ok": True})
    except Exception as exc:
        app.logger.exception("Telegram send failed")
        return jsonify({"ok": False, "error": str(exc)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "8080")))