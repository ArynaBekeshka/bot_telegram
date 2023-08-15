import telebot
from config import keys, TOKEN
from Exeptions import CryptoConverter, APIException


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'actions'])
def actions(message: telebot.types.Message):
    text = 'Добрый день! Если вы хотите начать работу с ботом введите команду в следующем формате (через пробел):' \
           ' \n- <Введите валюту, которую хотите перевести>  \n- <Введите название валюты,  lkz результат ' \
           'Курс:> \n- <Сумма перевода?>\n \
 Доступные валюты: /values'

    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def get_price(message: telebot.types.Message):
    try:
        words = message.text.split(' ')

        if len(words) != 3:
            raise APIException('Введено неправильное кол-во параметров, попробуйте снова')

        base, quote, amount = words

        total_base = CryptoConverter.get_price(base, quote, amount)
    except APIException as e:
        error_message = f'Ошибка пользователя: {e}'
        print(error_message)
        bot.reply_to(message, error_message)
    except Exception as e:
        error_message = f'Не удалось обработать команду: {e}'
        print(error_message)
        bot.reply_to(message, error_message)
    else:
        result_message = f'Цена {amount} {base} в {quote}: {total_base}'
        print(result_message)
        bot.send_message(message.chat.id, result_message)

        final_message = f'Итог: {amount} {base} = {total_base} {quote}'
        bot.send_message(message.chat.id, final_message)
        print(final_message)


bot.polling(none_stop=True)
