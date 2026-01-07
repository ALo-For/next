import telebot
from telebot import types
import requests
import json
import phonenumbers
from phonenumbers import carrier, geocoder, timezone

TOKEN = "6473126816:AAHUh0DXTqV2hOZgpCMJnaoT9qFTF-t1YjU"
bot = telebot.TeleBot(TOKEN)

# ======== واجهة البداية ========
@bot.message_handler(commands=['start'])
def menu(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("📱 معلومات رقم", callback_data="phone_info")
    btn2 = types.InlineKeyboardButton("🎵 تيك توك", callback_data="tiktok_info")
    ch = types.InlineKeyboardButton("قناتنا", url="https://t.me/QUU1Q")
    markup.add(btn1, btn2)
    markup.add(ch)
    bot.send_message(message.chat.id, "اختر نوع المعلومات:", reply_markup=markup)

# ======== أزرار التحكم ========
@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data == "phone_info":
        bot.send_message(call.message.chat.id, "أرسل رقم الهاتف الآن:")
        bot.register_next_step_handler(call.message, phone_lookup)
    elif call.data == "tiktok_info":
        bot.send_message(call.message.chat.id, "أرسل يوزر التيك توك الآن:")
        bot.register_next_step_handler(call.message, tiktok_lookup)

# ======== معلومات الرقم ========
def phone_lookup(message):
    User_phone = message.text.strip()
    default_region = "US"
    try:
        parsed_number = phonenumbers.parse(User_phone, default_region)
        region_code = phonenumbers.region_code_for_number(parsed_number)
        jenis_provider = carrier.name_for_number(parsed_number, "en")
        location = geocoder.description_for_number(parsed_number, "en")
        timezone1 = timezone.time_zones_for_number(parsed_number)
        timezoneF = ', '.join(timezone1)
        is_valid_number = phonenumbers.is_valid_number(parsed_number)
        is_possible_number = phonenumbers.is_possible_number(parsed_number)

        response = (
            f"📌 **معلومات الرقم:**\n\n"
            f"• الدولة: {location}\n"
            f"• رمز المنطقة: {region_code}\n"
            f"• التوقيت: {timezoneF}\n"
            f"• شركة الاتصال: {jenis_provider}\n"
            f"• صالح: {is_valid_number}\n"
            f"• ممكن: {is_possible_number}\n"
            f"• الرقم الدولي: {phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)}\n"
        )

        markup = types.InlineKeyboardMarkup()
        whatsapp_button = types.InlineKeyboardButton("واتساب", url=f"https://wa.me/{parsed_number.national_number}")
        telegram_button = types.InlineKeyboardButton("تيلجرام", url=f"https://t.me/{User_phone}")
        markup.add(whatsapp_button, telegram_button)

        bot.send_message(message.chat.id, response, reply_markup=markup, parse_mode="Markdown")
    except:
        bot.reply_to(message, "❌ الرقم غير صالح.")

# ======== تيك توك ========
def tiktok_lookup(message):
    username = message.text.strip()
    my = types.InlineKeyboardButton(text='قناتي', url="t.me/adoat1")
    xr = types.InlineKeyboardMarkup()
    acc = types.InlineKeyboardButton(text='دخول للحساب', url=f'https://tiktok.com/@{username}')
    xr.row(acc, my)

    # الحصول على بيانات التيك توك
    ur = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/signupNewUser"
    dat = {'key': "AIzaSyAZqmylIOE4fQmf0pemugc2iBH33rSeMkg"}
    dataa = json.dumps({"returnSecureToken": True})
    he = {
        'User-Agent': "okhttp/3.12.1",
        'Accept-Encoding': "gzip",
        'Content-Type': "application/json",
        'x-client-version': "ReactNative/JsCore/7.8.1/FirebaseCore-web"
    }
    res = requests.post(ur, params=dat, data=dataa, headers=he)
    res.raise_for_status()
    token = res.json().get("idToken")

    url = "https://us-central1-tikfans-prod-a3557.cloudfunctions.net/getTikTokUserInfo"
    data = json.dumps({"data": {"username": username}})
    he = {
        'User-Agent': "okhttp/3.12.1",
        'Accept-Encoding': "gzip",
        'Content-Type': "application/json",
        'authorization': f"Bearer {token}"
    }
    re = requests.post(url, data=data, headers=he)
    re.raise_for_status()
    data = re.json()

    ff = f"{data['result']['coversMedium'][0]}"
    usse = (
        f"Username: {data['result']['uniqueId']}\n"
        f"User ID: {data['result']['userId']}\n"
        f"Nickname: {data['result']['nickName']}\n"
        f"Following: {data['result']['following']}\n"
        f"Fans: {data['result']['fans']}\n"
        f"Videos: {data['result']['video']}\n"
        f"Signature: {data['result']['signature']}\n"
        f"Hearts: {data['result']['heart']}\n"
        f"Digg: {data['result']['digg']}\n"
        f"Secret Account: {data['result']['isSecret']}\n"
        f"SecUID: {data['result']['secUid']}\n"
        f"Open Favorite: {data['result']['openFavorite']}"
    )
    bot.send_photo(message.chat.id, ff, caption=usse, reply_markup=xr)

# ======== تشغيل البوت ========
bot.infinity_polling()
