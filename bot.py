import telebot
from config import TOKEN, KEYS
from extensions import CurrencyConvertor, APIException

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = ''''Бот производит конвертацию из одной валюты в другую.\n\n \
    Список доступных для конвертации валют: /values\n\
    Для конвертации напишите боту в следующем формате:\n\n<имя валюты> \
    <в какую валюту перевести> <количество переводимой валюты>\n\n \
    Доступные команды:\n/values - \
    список доступных валют.\n/help - помощь.'''
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = '''Доступные валюты: '''
    for key in KEYS.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.lower().split(' ')

        if len(values) != 3:
            raise APIException('''Неверное количество параметров.''')

        quote, base, amount = values
        total_base = CurrencyConvertor.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'''Ошибка пользователя.\n{e}''')
    except Exception as e:
        bot.reply_to(message, f'''Не удалось обработать команду.\n{e}''')
    else:
        text = f'''Цена {amount} {KEYS[quote]} = {total_base} {KEYS[base]}'''
        bot.send_message(message.chat.id, text)


bot.polling()