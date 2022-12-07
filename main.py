# developed by strelnikov87
import telebot
from extensions import SymbolPrice, APIException
from settings import TG_TOKEN


bot = telebot.TeleBot(TG_TOKEN)


@bot.message_handler(commands=['start', 'help'])
def test_func(message: telebot.types.Message):
    bot.send_message(message.chat.id, 'Чтобы вывести список валют, \
введите команду /values.\nХотите узнать стоимость валюты? \nВведите тикер базовой валюты, \
конвертируемой валюты и количество.\nприм.: USD RUB 1')


@bot.message_handler(commands=['values'])
def value_list(message: telebot.types.Message):
    bot.send_message(message.chat.id, 'Валюты:\nEUR - Евро\nUSD - Доллар\nRUB - Рубль')


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        if len(values) != 3:
            raise APIException('Введено неверное количество параметров!')
        base, quote, amount = values
        response = SymbolPrice.get_price(base, quote, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка ползователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        bot.send_message(message.chat.id, response)


bot.polling()
