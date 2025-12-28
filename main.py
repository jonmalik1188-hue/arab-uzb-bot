import telebot
from telebot import types
from deep_translator import GoogleTranslator

# ====== SOZLAMALAR ======
TOKEN = "8316384727:AAF2gCkmirf0-JsjmxjeJQNrhEw9i-0JLw4"
CHANNEL_USERNAME = "@Rahmatulloh_arabic"
LIMIT = 10

bot = telebot.TeleBot(TOKEN)

user_count = {}

# ====== OBUNA TEKSHIRISH ======
def check_sub(chat_id):
    try:
        status = bot.get_chat_member(CHANNEL_USERNAME, chat_id).status
        return status in ["member", "administrator", "creator"]
    except:
        return False

# ====== START ======
@bot.message_handler(commands=['start'])
def start(message):
    user_count[message.chat.id] = 0
    bot.send_message(
        message.chat.id,
        "👋 Assalomu alaykum!\n\n"
        "🟢 Arab ↔ O‘zbek tarjima bot\n\n"
        "✍️ Matn yuboring, men tarjima qilaman.\n"
        "⚠️ 10 ta so‘rovdan keyin kanalga obuna talab qilinadi."
    )

# ====== TARJIMA ======
@bot.message_handler(func=lambda m: True)
def translate(message):
    uid = message.chat.id

    if uid not in user_count:
        user_count[uid] = 0

    # limit tekshirish
    if user_count[uid] >= LIMIT:
        if not check_sub(uid):
            markup = types.InlineKeyboardMarkup()
            markup.add(
                types.InlineKeyboardButton(
                    "📢 Kanalga obuna bo‘lish",
                    url="https://t.me/Rahmatulloh_arabic"
                )
            )
            bot.send_message(
                uid,
                "❌ Siz 10 ta tarjimadan foydalandingiz.\n\n"
                "✅ Davom etish uchun kanalga obuna bo‘ling:",
                reply_markup=markup
            )
            return

    text = message.text.strip()

    try:
        # Arab → O‘zbek yoki O‘zbek → Arab aniqlash
        if any('\u0600' <= c <= '\u06FF' for c in text):
            result = GoogleTranslator(source='ar', target='uz').translate(text)
            lang = "🇸🇦 Arab → 🇺🇿 O‘zbek"
        else:
            result = GoogleTranslator(source='uz', target='ar').translate(text)
            lang = "🇺🇿 O‘zbek → 🇸🇦 Arab"

        user_count[uid] += 1

        bot.send_message(
            uid,
            f"🔁 {lang}\n\n"
            f"📝 Matn:\n{text}\n\n"
            f"✅ Tarjima:\n{result}\n\n"
            f"📊 Hisob: {user_count[uid]}/{LIMIT}"
        )

    except Exception as e:
        bot.send_message(uid, "❌ Xatolik yuz berdi, keyinroq urinib ko‘ring.")

# ====== ISHGA TUSHIRISH ======
bot.infinity_polling()
python main.py
