import telebot
import requests
import json

API_TOKEN = '6242446698:AAE16Ubl7fiYZabQ0rJRe54DCgrsvM7TzXk'

bot = telebot.TeleBot(API_TOKEN)

def get_balance(api_key):
    url = f'https://kodeotp.com/api?api_key={api_key}&action=balance'
    response = requests.get(url)
    data = json.loads(response.text)
    saldo = int(float(data['data']['balance']))
    formatted_saldo = f"Rp {saldo:,}".replace(",", ".")
    return formatted_saldo

def get_country_list(api_key):
    url = f'https://kodeotp.com/api?api_key={api_key}&action=country'
    response = requests
    response = requests.get(url)
    data = json.loads(response.text)
    country_list = data['data']
    formatted_country_list = "\n".join([f"{country['country_id']}. {country['name']}" for country in country_list])
    return formatted_country_list

def send_paginated_country_list(chat_id, message_id=None, offset=0, step=10):
    api_key = '73de2d7580ec0ed58df2795ebfd1703c'
    country_list = get_country_list(api_key)
    paginated_list = country_list.split("\n")[offset:offset + step]

    if not paginated_list:
        return

    formatted_list = "\n".join(paginated_list)

    markup = telebot.types.InlineKeyboardMarkup()
    if offset > 0:
        markup.add(telebot.types.InlineKeyboardButton("⬅️ Kembali", callback_data=f"prev_{offset - step}"))
    if len(country_list.split("\n")) > offset + step:
        markup.add(telebot.types.InlineKeyboardButton("Lanjutkan ➡️", callback_data=f"next_{offset + step}"))

    if message_id:
        bot.edit_message_text(f"Daftar Negara:\n{formatted_list}", chat_id, message_id, reply_markup=markup)
    else:
        sent_message = bot.send_message(chat_id, f"Daftar Negara:\n{formatted_list}", reply_markup=markup)
        message_id = sent_message.message_id
    return message_id

def get_price_list(api_key, country_id):
    url = f'https://kodeotp.com/api?api_key={api_key}&action=get_service&country_id={country_id}&type=regular'
    response = requests.get(url)
    data = json.loads(response.text)
    price_list = data['data']
    formatted_price_list = "\n".join([f"{service['service_name']} - {service['cost']} (Stok: {service['count']})" for service in price_list])
    return formatted_price_list

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Selamat datang! Untuk mengecek saldo, ketik /saldo. Untuk melihat daftar negara, ketik /listnegara.")

@bot.message_handler(commands=['saldo'])
def send_saldo(message):
    api_key = '73de2d7580ec0ed58df2795ebfd1703c'
    try:
        saldo = get_balance(api_key)
        bot.reply_to(message, f"Saldo Anda: {saldo}")
    except Exception as e:
        bot.reply_to(message, f"Terjadi kesalahan saat mengambil saldo. Silakan coba lagi nanti.\nError: {e}")

@bot.message_handler(commands=['listnegara'])
def send_listnegara(message):
    try:
        send_paginated_country_list(message.chat.id)
    except Exception as e:
        bot.reply_to(message, f"Terjadi kesalahan saat mengambil daftar negara. Silakan coba lagi nanti.\nError: {e}")

@bot.callback_query_handler(func=lambda call: call.data.startswith("prev_") or call.data.startswith("next_"))
def handle_navigation(call):
    action, offset = call.data.split("_")
    offset = int(offset)
    bot.answer_callback_query(call.id)
    send_paginated_country_list(call.message.chat.id, message_id=call.message.message_id, offset=offset)
@bot.message_handler(commands=['listharga'])
def send_listharga(message):
    try:
        country_id = message.text.split()[1]  # Ambil parameter country_id dari pesan
        price_list = get_price_list('73de2d7580ec0ed58df2795ebfd1703c', country_id)
        bot.reply_to(message, f"Daftar Harga:\n{price_list}")
    except IndexError:
        bot.reply_to(message, "Format perintah salah. Gunakan format: /listharga <country_id>")
    except Exception as e:
        bot.reply_to(message, f"Terjadi kesalahan saat mengambil daftar harga. Silakan coba lagi nanti.\nError: {e}")
bot.polling()
