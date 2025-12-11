import telebot
from telebot import types

bot = telebot.TeleBot('8245986577:AAGcPG658n2542sdr8R-UAvO04586hqedyk')

@bot.message_handler(commands=['inform'])
def inform(message):
    inline_btn = types.InlineKeyboardButton("Отримати фото", callback_data='send_local_photo')
    inline_keyboard = types.InlineKeyboardMarkup().add(inline_btn)

    bot.send_message(message.chat.id, "Натисніть кнопку, щоб отримати фото:", reply_markup=inline_keyboard)

@bot.message_handler(commands=['keyboards'])
def keyboards(message):
    menu = types.InlineKeyboardMarkup()
    menu.add(
        types.InlineKeyboardButton("3 кнопки", callback_data="kb_3"),
        types.InlineKeyboardButton("4 кнопки", callback_data="kb_4"),
        types.InlineKeyboardButton("5 кнопок", callback_data="kb_5")
    )
    bot.send_message(message.chat.id, "Оберіть формат клавіатури:", reply_markup=menu)

@bot.message_handler(commands=['help'])
def help_cmd(message):
    text = (
        "*Доступні команди:*\n\n"
        "/help — показати список команд\n"
        "/inform — отримати інлайн-кнопку для надсилання JPG-фото\n"
        "/keyboards — вибір клавіатур через інлайн-кнопки\n"
    )
    bot.send_message(message.chat.id, text, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):

    if call.data == 'send_local_photo':
        try:
            with open("image.jpg", 'rb') as photo:
                bot.send_photo(call.message.chat.id, photo)
            bot.answer_callback_query(call.id, "Фото надіслано!")
        except FileNotFoundError:
            bot.answer_callback_query(call.id, "Файл image.jpg не знайдено!")
        return

    if call.data.startswith("kb_"):
        kb_type = call.data

        # 3 кнопки в 1 рядку
        if kb_type == "kb_3":
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
            kb.row("К1", "К2", "К3")
            bot.send_message(call.message.chat.id, "Клавіатура: 3 кнопки", reply_markup=kb)

        # 4 кнопки (формат 1×3)
        elif kb_type == "kb_4":
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
            kb.row("A")
            kb.row("B", "C", "D")
            bot.send_message(call.message.chat.id, "Клавіатура: 1×3", reply_markup=kb)

        # 5 кнопок (формат 2×3)
        elif kb_type == "kb_5":
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
            kb.row("X1", "X2")
            kb.row("X3", "X4", "X5")
            bot.send_message(call.message.chat.id, "Клавіатура: 2×3", reply_markup=kb)

        bot.answer_callback_query(call.id)


bot.polling(none_stop=True)
