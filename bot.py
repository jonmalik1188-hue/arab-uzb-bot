import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters
from deep_translator import GoogleTranslator

TOKEN = os.getenv("BOT_TOKEN")
CHANNEL = os.getenv("CHANNEL")

user_count = {}

def is_arabic(text):
    return any('\u0600' <= ch <= '\u06FF' for ch in text)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Assalomu alaykum!\n\n"
        "🇸🇦 ↔ 🇺🇿 Arabcha–O‘zbekcha tarjimon bot\n\n"
        "✍️ Matn yuboring — tarjima qilib beraman"
    )

async def translate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_count[user_id] = user_count.get(user_id, 0) + 1

    if user_count[user_id] > 10:
        try:
            member = await context.bot.get_chat_member(CHANNEL, user_id)
            if member.status not in ["member", "administrator", "creator"]:
                await update.message.reply_text(
                    f"🔔 Davom etish uchun kanalga obuna bo‘ling:\n"
                    f"https://t.me/Rahmatulloh_arabic"
                )
                return
        except:
            await update.message.reply_text(
                f"🔔 Avval kanalga obuna bo‘ling:\n"
                f"https://t.me/Rahmatulloh_arabic"
            )
            return

    text = update.message.text

    try:
        if is_arabic(text):
            result = GoogleTranslator(source="ar", target="uz").translate(text)
            await update.message.reply_text(f"🇸🇦 → 🇺🇿\n\n{result}")
        else:
            result = GoogleTranslator(source="uz", target="ar").translate(text)
            await update.message.reply_text(f"🇺🇿 → 🇸🇦\n\n{result}")
    except:
        await update.message.reply_text("❌ Tarjima vaqtida xatolik yuz berdi")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, translate))
app.run_polling()
