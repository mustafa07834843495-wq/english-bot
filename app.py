# -*- coding: utf-8 -*-
import os
import uuid
import threading
from datetime import datetime

from flask import Flask

import telebot
from telebot.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from PIL import Image
from fpdf import FPDF

# ========= غير التوكن فقط =========
TOKEN = "8444169687:AAGrqIQqDoFdMQ6sMTcJBoXm9FboJq2IFnU"
# =================================

ANON_BOT_USERNAME = "u676u_Bot"  # بدون @

# Flask server (Ping endpoint)
server = Flask(__name__)

@server.get("/")
def home():
    return "OK", 200

@server.get("/health")
def health():
    return "OK", 200


bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

MODE = {}       # user_id -> "pdf" / None
PDF_IMGS = {}   # user_id -> [paths]


WELCOME_TEXT = """أهلاً وسهلاً بك في بوت قسم اللغة الإنكليزية
هذا البوت تم إنشاؤه لمساعدتكم وتسهيل الوصول للخدمات المهمة ..

📌 <b>الخدمات المتوفرة داخل البوت:</b>
📚 قنوات القسم الأساسية
🎓 القنوات التعليمية
📞 تواصل ممثلي الشعب
✉️ إرسال رسالة مجهولة
🖼️ تحويل الصور إلى PDF

البوت خاص بالمرحلة الثانية ويتم تحديثه بشكل مستمر خلال كل سنة دراسية من قبل الممثل العام (مصطفى حاتم) .
"""

BASIC_CHANNELS_TEXT = """📚 <b>القنوات الأساسية</b>

🔹 قناة قسم اللغة الانكليزية
https://t.me/Mustafa_Hatem

🔹 قناة الممثل
https://t.me/mu6staf

🔹 المجموعة العامة
https://t.me/Mustafa_Hatttem
"""

EDU_CHANNELS_TEXT = """📘 <b>القنوات التعليمية - قسم اللغة الانكليزية</b>

• مادة الصوت
https://t.me/c/2996295064/49

• مادة الإنشاء
https://t.me/Anmarsec

• مادة الشعر
https://t.me/+S1YjaXQypxNmNTJi

• مادة طرائق التدريس
https://t.me/Elts2stage

• مادة الاستيعاب
https://t.me/s5_0000

• مادة الدراما
د.هدى: https://t.me/drama2ndstage2025
د.فرح: https://t.me/+K5dbeuMGyqgyZmQ6

• مادة القصة القصيرة
https://t.me/+iTyuZy9VvSw0ZjMy

• مادة علم النفس
https://t.me/+E9cHARycd400YTNi

• مادة النحو
https://t.me/+xufVSwAYHFY2ZjIy

• قناة الشروحات
https://t.me/Mustafa_29Hatem
"""

REPRESENTATIVES_TEXT = """📞 <b>تواصل ممثلي الشعب</b>

👤 الممثل العام :
الاسم: مصطفى حاتم طه
📱 الرقم: 07734784094

👤 ممثل G1:
الاسم: أيوب ابراهيم كاظم
📱 الرقم: 07500842762

👤 ممثل G2:
الاسم: —
📱 الرقم: 07XXXXXXXXX

👤 ممثل G3:
الاسم: سجاد احمد جواد
📱 الرقم: 07780153561

👤 ممثل G4:
الاسم: عبدالله ماجد شمخي
📱 الرقم: 07765199959

👤 ممثل G5:
الاسم: محمد عماد محمد
📱 الرقم: 07805190913

👤 ممثل G6:
الاسم: هارف خالد حميد
📱 الرقم: 07804480233

👤 ممثل G7:
الاسم: حيدر صالح محسن
📱 الرقم: 07505112509

👤 ممثل G8:
الاسم: يعقوب صباح حسن
📱 الرقم: 07860539065

👤 ممثل G9:
الاسم: دنيا عبدالله براهيم
📱 الرقم: 07832902039

⏰ يرجى الاتصال ضمن الأوقات المناسبة
"""


def main_keyboard():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row(KeyboardButton("📚 قنوات القسم الأساسية"), KeyboardButton("🎓 القنوات التعليمية"))
    kb.row(KeyboardButton("📞 تواصل ممثلي الشعب"))
    kb.row(KeyboardButton("✉️ إرسال رسالة مجهولة"))
    kb.row(KeyboardButton("🖼️ تحويل الصور إلى PDF"), KeyboardButton("✅ إنهاء PDF"))
    return kb


def reset_pdf(user_id: int):
    paths = PDF_IMGS.get(user_id, [])
    for p in paths:
        try:
            os.remove(p)
        except Exception:
            pass
    PDF_IMGS[user_id] = []


@bot.message_handler(commands=["start"])
def start(message):
    MODE[message.from_user.id] = None
    bot.send_message(message.chat.id, WELCOME_TEXT, reply_markup=main_keyboard())


@bot.message_handler(func=lambda m: (m.text or "").strip() == "بوت")
def show_menu_on_word_bot(message):
    bot.send_message(message.chat.id, "تفضل القائمة 👇", reply_markup=main_keyboard())


@bot.message_handler(func=lambda m: m.text == "📚 قنوات القسم الأساسية")
def basic_channels(message):
    MODE[message.from_user.id] = None
    bot.send_message(message.chat.id, BASIC_CHANNELS_TEXT, reply_markup=main_keyboard())


@bot.message_handler(func=lambda m: m.text == "🎓 القنوات التعليمية")
def edu_channels(message):
    MODE[message.from_user.id] = None
    bot.send_message(message.chat.id, EDU_CHANNELS_TEXT, reply_markup=main_keyboard())


@bot.message_handler(func=lambda m: m.text == "📞 تواصل ممثلي الشعب")
def representatives(message):
    MODE[message.from_user.id] = None
    bot.send_message(message.chat.id, REPRESENTATIVES_TEXT, reply_markup=main_keyboard())


@bot.message_handler(func=lambda m: m.text == "✉️ إرسال رسالة مجهولة")
def anon_redirect(message):
    MODE[message.from_user.id] = None
    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton(
            "✉️ افتح بوت الرسائل المجهولة",
            url=f"https://t.me/{ANON_BOT_USERNAME}?start=from_main_bot",
        )
    )
    bot.send_message(
        message.chat.id,
        "✉️ لإرسال رسالة مجهولة اضغط الزر بالأسفل 👇\n"
        f"أو ادخل مباشرة: @{ANON_BOT_USERNAME}",
        reply_markup=kb,
    )


@bot.message_handler(func=lambda m: m.text == "🖼️ تحويل الصور إلى PDF")
def pdf_mode(message):
    user_id = message.from_user.id
    MODE[user_id] = "pdf"
    PDF_IMGS.setdefault(user_id, [])
    bot.send_message(
        message.chat.id,
        "🖼️ ارسل الصور (واحدة أو أكثر)، وبعدها اضغط ✅ إنهاء PDF",
        reply_markup=main_keyboard(),
    )


@bot.message_handler(content_types=["photo"])
def handle_photo(message):
    user_id = message.from_user.id
    if MODE.get(user_id) != "pdf":
        return

    PDF_IMGS.setdefault(user_id, [])

    file_id = message.photo[-1].file_id
    file_info = bot.get_file(file_id)
    downloaded = bot.download_file(file_info.file_path)

    os.makedirs("tmp_imgs", exist_ok=True)
    path = os.path.join("tmp_imgs", f"{uuid.uuid4().hex}.jpg")
    with open(path, "wb") as f:
        f.write(downloaded)

    PDF_IMGS[user_id].append(path)
    bot.reply_to(message, f"✅ تم استلام الصورة ({len(PDF_IMGS[user_id])})")


@bot.message_handler(func=lambda m: m.text == "✅ إنهاء PDF")
def finish_pdf(message):
    user_id = message.from_user.id
    paths = PDF_IMGS.get(user_id, [])

    if not paths:
        bot.send_message(message.chat.id, "⚠️ ما مستلم صور بعد.", reply_markup=main_keyboard())
        return

    try:
        pdf = FPDF(unit="pt", format="A4")
        page_w, page_h = 595, 842  # A4

        for p in paths:
            img = Image.open(p).convert("RGB")

            tmp = p + ".jpg"
            img.save(tmp, "JPEG", quality=95)

            pdf.add_page()
            pdf.image(tmp, x=0, y=0, w=page_w, h=page_h)

            try:
                os.remove(tmp)
            except Exception:
                pass

        out_name = f"images_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        pdf.output(out_name)

        with open(out_name, "rb") as f:
            bot.send_document(message.chat.id, f, caption="✅ تم تحويل الصور إلى PDF")

        try:
            os.remove(out_name)
        except Exception:
            pass

        reset_pdf(user_id)
        MODE[user_id] = None

    except Exception as e:
        bot.send_message(message.chat.id, f"❌ صار خطأ بالتحويل: {e}", reply_markup=main_keyboard())


@bot.message_handler(content_types=["text"])
def fallback_text(message):
    bot.send_message(message.chat.id, "اختار من الأزرار بالأسفل 👇", reply_markup=main_keyboard())


def _run_bot_polling_once():
    bot.infinity_polling(timeout=60, long_polling_timeout=60)


_thread_started = False

@server.before_request
def _start_bot_thread_if_needed():
    global _thread_started
    if _thread_started:
        return
    _thread_started = True
    t = threading.Thread(target=_run_bot_polling_once, daemon=True)
    t.start()
