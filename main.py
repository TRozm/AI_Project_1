import telebot
from telebot import types

bot = telebot.TeleBot('8245986577:AAGcPG658n2542sdr8R-UAvO04586hqedyk')
photo_url = 'https://upload.wikimedia.org/wikipedia/commons/thumb/2/24/LEGO_logo.svg/1024px-LEGO_logo.svg.png'
@bot.message_handler(commands=['start'])
def hello(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=False)
    keyboard.add(types.KeyboardButton('Відправити картинку'),types.KeyboardButton('Відправити файл'))
    keyboard.add(types.KeyboardButton('Відповісти на питання'))
    bot.send_message(message.chat.id, f'Привіт {message.from_user.first_name}!', reply_markup=keyboard)
@bot.message_handler(content_types=['text'])
def main_menu(message):
    if message.text == 'Відправити картинку':
        bot.send_photo(message.chat.id, photo=photo_url, caption='Це логотип!')
    elif message.text == 'Відправити файл':
        f = open('test.txt', 'rb')
        bot.send_document(message.chat.id, document=f, caption='Важливий файл!')
        f.close() # Не забудьте закрити файл після відправлення
    elif message.text == 'Відповісти на питання':
        inlineKeyboard = types.InlineKeyboardMarkup()
        inlineKeyboard.add(types.InlineKeyboardButton('2', callback_data='2'))
        inlineKeyboard.add(types.InlineKeyboardButton('4', callback_data='4'))
        inlineKeyboard.add(types.InlineKeyboardButton('5', callback_data='5'))
        bot.send_message(message.chat.id, '2+2=?', reply_markup=inlineKeyboard)
# Додаємо обробник callback-ів для Inline-кнопок
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == '2':
        bot.answer_callback_query(call.id, "Неправильно!")
    elif call.data == '4':
        bot.answer_callback_query(call.id, "Правильно!")
    elif call.data == '5':
        bot.answer_callback_query(call.id, "Неправильно!")

bot.polling(none_stop=True)