import telebot
from config import keys, TOKEN
from extensions import ConvertionException, CryptoConverter

bot = telebot.TeleBot(TOKEN)
@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    text = "Чтобы начать работу, введите команду боту в следущем виде через пробел: \n <Имя валюты> \
<В какую валюты хотите перевести><количество валюты для рассчета>\nПример: биткоин доллар 2\n Увидеть список всех доступных валют: /values"
    bot.reply_to(message, text)
@bot.message_handler(commands=["values"])
def values(message: telebot.types.Message):
    text = "Доступные валюты:"
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)
@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values_mix = message.text.split(' ')
        values = []
        for i in values_mix:
            b = i.lower()
            values.append(b)

        if len(values) != 3:
            raise ConvertionException('Введите команду или 3 параметра')
        quote, base, amount = values
        total_base = CryptoConverter.convert(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Что-то пошло не так с {e}')
    else:
        text = f'Цена {amount} {quote} в {base} составляет {total_base}'
        bot.send_message(message.chat.id, text)



bot.polling(none_stop=True)