"""
نقطه‌ی ورود اصلی بات تلگرام.

قابلیت‌ها:
  1. پاسخ خودکار بر اساس کلیدواژه‌های از پیش تعیین‌شده (در responses.py) —
     فعلاً به جای AI از این استفاده می‌کنیم؛ هر وقت خواستید می‌شه AI رو
     دوباره وصل کرد (فایل ai_responder.py نگه داشته نشده، در صورت نیاز بسازید)
  2. گزارش روزانه‌ی قیمت دلار/طلا/ارز دیجیتال برای صاحب بات
  3. چک دوره‌ای سایت‌های کاریابی برای پروژه‌های جدید

اجرا:
    export TELEGRAM_BOT_TOKEN="8976588548:AAHUuhYRTYJrB1qEZYIHApoPijsk3VhpoJI"
    export OWNER_CHAT_ID="7935813308"
    python bot.py

این بات باید به‌صورت مداوم روی یه سرویس (سرور شخصی، VPS یا پلتفرمی مثل
Railway/Render) در حال اجرا بمونه. جزئیات در README.md توضیح داده شده.
"""
import logging

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from config import (
    DAILY_PRICE_REPORT_HOUR,
    JOB_CHECK_INTERVAL_HOURS,
    OWNER_CHAT_ID,
    TELEGRAM_BOT_TOKEN,
)
from responses import FIXED_RESPONSES, DEFAULT_RESPONSE
from price_fetcher import format_price_report
from job_scraper import fetch_new_jobs, format_jobs_message

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


# ---------- دستورات کاربر ----------

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "سلام! من دستیار هوشمند این کسب‌وکار هستم. سوالتون رو بپرسید تا کمکتون کنم 🙂"
    )


async def price_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """دستور /price برای گرفتن فوری گزارش کامل (دلار، طلا، ارز دیجیتال برتر)."""
    await update.message.reply_text("در حال دریافت قیمت‌ها...")
    report = format_price_report()
    await update.message.reply_text(report)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """پیام کاربر رو با کلیدواژه‌های تعریف‌شده در responses.py مقایسه می‌کنه
    و جواب مناسب رو می‌فرسته. اگه هیچ کلیدواژه‌ای پیدا نشد، جواب پیش‌فرض می‌ره."""
    text = (update.message.text or "").strip().lower()

    for keyword, response in FIXED_RESPONSES.items():
        if keyword in text:
            await update.message.reply_text(response)
            return

    await update.message.reply_text(DEFAULT_RESPONSE)


# ---------- وظایف زمان‌بندی‌شده ----------

async def daily_price_job(context: ContextTypes.DEFAULT_TYPE) -> None:
    if not OWNER_CHAT_ID:
        logger.warning("OWNER_CHAT_ID تنظیم نشده، گزارش قیمت ارسال نشد.")
        return
    report = format_price_report()
    await context.bot.send_message(chat_id=OWNER_CHAT_ID, text=report)


async def job_check_task(context: ContextTypes.DEFAULT_TYPE) -> None:
    if not OWNER_CHAT_ID:
        logger.warning("OWNER_CHAT_ID تنظیم نشده، نتیجه چک پروژه‌ها ارسال نشد.")
        return
    new_jobs = fetch_new_jobs()
    if new_jobs:
        await context.bot.send_message(
            chat_id=OWNER_CHAT_ID, text=format_jobs_message(new_jobs)
        )
    else:
        logger.info("پروژه جدیدی پیدا نشد.")


def main() -> None:
    if not TELEGRAM_BOT_TOKEN:
        raise SystemExit("لطفاً TELEGRAM_BOT_TOKEN رو تنظیم کنید.")

    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("price", price_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    job_queue = app.job_queue
    job_queue.run_repeating(
        job_check_task, interval=JOB_CHECK_INTERVAL_HOURS * 3600, first=10
    )
    job_queue.run_daily(
        daily_price_job,
        time=__import__("datetime").time(hour=DAILY_PRICE_REPORT_HOUR, minute=0),
    )

    logger.info("بات در حال اجراست...")
    app.run_polling()


if __name__ == "__main__":
    main()
