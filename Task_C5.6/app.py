import telebot
from config import keys, TOKEN
from extensions import ConvertionException, Cryptoconverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands = ['start', 'help'])
def echo_test(message: telebot.types.Message):
    text = 'Чтобы начать работу, введите команду боту в следующем формате:\n<имя валюты> \
<в какую валюту перевести> \
<количество переводимой валюты>\nУвидеть список всех доступных валют: /values'
    bot.reply_to(message, text)
    

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    values = message.text.split(' ')
    try:
        if len(values) > 3:
            raise ConvertionException('Слишком много параметров.')
        if len(values) < 3:
            raise ConvertionException('Слишком мало параметров.')
        quote, base, amount = values
        total_base = Cryptoconverter.get_price(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')     
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:    
        text = f'Цена {amount} {quote} в {base} - {total_base}'            
        bot.send_message(message.chat.id, text)

bot.polling()    