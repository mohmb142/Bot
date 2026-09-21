# TradingView → Telegram Signal Bot

هذا المستودع يحوّل إشارات المؤشر إلى رسائل Telegram عبر Webhook.

## البنية
TradingView → Webhook → Flask → Telegram Bot

البوت لا يعيد حساب المؤشر. ملف Pine يحافظ على منطق BUY/SELL وWIN/LOSS الأصلي، وتضاف فقط طبقة التنبيه.

## الأحداث
- signal: عند ظهور BUY أو SELL.
- confirmed: عند إغلاق الشمعة إذا بقيت الإشارة موجودة.
- cancelled: إذا ظهرت الإشارة ثم اختفت قبل الإغلاق.

## الملفات
- app.py: خادم Webhook وإرسال Telegram.
- pine/dollar_indicators_telegram.pine: المؤشر الأصلي مع طبقة التنبيه فقط.
- requirements.txt: الاعتمادات.
- Procfile: أمر التشغيل على خدمات الاستضافة التي تدعم Gunicorn.
- .env.example: أسماء المتغيرات السرية.

## المتغيرات
TELEGRAM_BOT_TOKEN
TELEGRAM_CHAT_ID
WEBHOOK_SECRET
PORT

لا تضع توكن Telegram داخل GitHub أو Pine Script.

## TradingView
بعد نشر الخادم، أنشئ Alert على المؤشر واختر Any alert() function call، ثم ضع رابط POST الخاص بـ /webhook في Webhook URL.

تنبيه مهم: Webhook من TradingView يرسل HTTP POST إلى خادمك، ويجب أن يكون الخادم متاحًا عبر HTTPS. كما أن TradingView توصي بحماية نقطة النهاية وعدم وضع بيانات حساسة داخل جسم الطلب.

هذا المشروع يرسل الإشارات فقط ولا ينفذ أي صفقة.