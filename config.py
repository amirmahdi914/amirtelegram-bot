"""
تنظیمات بات از طریق متغیرهای محیطی (Environment Variables) خونده می‌شن.
قبل از اجرا باید این مقادیر رو در یه فایل .env یا در سیستم‌عامل ست کنید.
"""
import os

# توکن بات تلگرام - از @BotFather بگیرید
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")

# نکته: فعلاً پاسخ‌گویی با AI غیرفعاله و جوابا از responses.py خونده می‌شن.
# هر وقت خواستید AI رو اضافه کنید، یه ANTHROPIC_API_KEY اینجا تعریف کنید.

# آیدی عددی چت/کاربری که گزارش‌ها (قیمت، فرصت‌های شغلی) براش ارسال بشه
# برای گرفتن آیدی‌تون می‌تونید به بات @userinfobot پیام بدید
OWNER_CHAT_ID = os.getenv("OWNER_CHAT_ID", "")

# هر چند ساعت یکبار سایت‌های کاریابی چک بشن
JOB_CHECK_INTERVAL_HOURS = float(os.getenv("JOB_CHECK_INTERVAL_HOURS", "3"))

# ساعت روزانه ارسال گزارش قیمت طلا/دلار (به وقت تهران، فرمت 24 ساعته)
DAILY_PRICE_REPORT_HOUR = int(os.getenv("DAILY_PRICE_REPORT_HOUR", "9"))

# کلمات کلیدی که توی عنوان پروژه‌های جاب‌ویژن دنبالشون می‌گردیم
JOB_KEYWORDS = [
    kw.strip()
    for kw in os.getenv("JOB_KEYWORDS", "طراحی سایت,طراحی وب,وب سایت,فرانت‌اند,React").split(",")
    if kw.strip()
]

# فایل ذخیره‌سازی وضعیت (پروژه‌های دیده‌شده) تا پیام تکراری ارسال نشه
STATE_FILE = os.getenv("STATE_FILE", "bot_state.json")
