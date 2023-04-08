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
    response = requests.get(url)
    data = json.loads(response.text)
    country_list = data['data']
    formatted_country_list = "\n".join([f"{index + 1}. {country['name']}" for index, country in enumerate(country_list)])
    return formatted_country_list

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
    api_key = '73de2d7580ec0ed58df2795ebfd1703c'
    try:
        list_negara = get_country_list(api_key)
        bot.reply_to(message, f"Daftar Negara:\n{list_negara}")
    except Exception as e:
        bot.reply_to(message, f"Terjadi kesalahan saat mengambil daftar negara. Silakan coba lagi nanti.\nError: {e}")

bot.polling()
