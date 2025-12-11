import telebot
from telebot import types
import sqlite3

bot = telebot.TeleBot('8245986577:AAGcPG658n2542sdr8R-UAvO04586hqedyk')

conn = sqlite3.connect("pet_orders.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
               CREATE TABLE IF NOT EXISTS users
               (
                   user_id
                   INTEGER
                   PRIMARY
                   KEY,
                   name
                   TEXT
               )
               """)

cursor.execute("""
               CREATE TABLE IF NOT EXISTS orders
               (
                   order_id
                   INTEGER
                   PRIMARY
                   KEY
                   AUTOINCREMENT,
                   user_id
                   INTEGER,
                   item
                   TEXT,
                   quantity
                   INTEGER,
                   status
                   TEXT
                   DEFAULT
                   'нове',
                   FOREIGN
                   KEY
               (
                   user_id
               ) REFERENCES users
               (
                   user_id
               )
                   )
               """)
conn.commit()

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("📦 Замовити корм", "📅 Запис на консультацію")
    markup.row("ℹ️ Інформація", "📢 Розсилка")
    bot.send_message(message.chat.id, "Вітаємо! Оберіть дію:", reply_markup=markup)

@bot.message_handler(commands=['help'])
def help_cmd(message):
    text = (
        "Доступні команди:\n"
        "/start — головне меню\n"
        "/help — допомога\n"
        "Використовуйте кнопки для замовлень та запису на консультації."
    )
    bot.send_message(message.chat.id, text)

@bot.message_handler(func=lambda message: True)
def menu_handler(message):
    if message.text == "📦 Замовити корм":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row("Сухий корм", "Вологий корм")
        markup.row("Назад ⬅️")
        bot.send_message(message.chat.id, "Оберіть тип корму:", reply_markup=markup)

    elif message.text in ["Сухий корм", "Вологий корм"]:
        bot.send_message(message.chat.id, f"Вкажіть кількість для {message.text}:")
        bot.register_next_step_handler(message, process_order, message.text)

    elif message.text == "📅 Запис на консультацію":
        bot.send_message(message.chat.id, "Вкажіть дату та час консультації:")
        bot.register_next_step_handler(message, process_appointment)

    elif message.text == "ℹ️ Інформація":
        bot.send_message(message.chat.id,
                         "Ми пропонуємо корм для собак та котів. Використовуйте кнопки меню для замовлення чи запису на консультацію.")

    elif message.text == "📢 Розсилка":
        bot.send_message(message.chat.id,
                         "Це буде розсилка актуальних пропозицій. Для прикладу надіслано повідомлення.")

    elif message.text == "Назад ⬅️":
        start(message)

def process_order(message, item):
    try:
        quantity = int(message.text)
    except ValueError:
        bot.send_message(message.chat.id, "Будь ласка, введіть числове значення.")
        bot.register_next_step_handler(message, process_order, item)
        return

    cursor.execute("INSERT OR IGNORE INTO users(user_id) VALUES (?)", (message.from_user.id,))
    conn.commit()

    cursor.execute(
        "INSERT INTO orders(user_id, item, quantity) VALUES (?, ?, ?)",
        (message.from_user.id, item, quantity)
    )
    conn.commit()

    bot.send_message(message.chat.id, f"Замовлення на {quantity} шт. {item} успішно додано!")
    start(message)


def process_appointment(message):
    cursor.execute("INSERT OR IGNORE INTO users(user_id) VALUES (?)", (message.from_user.id,))
    conn.commit()

    appointment_info = message.text
    bot.send_message(message.chat.id, f"Ви записані на консультацію: {appointment_info}")
    start(message)

bot.polling(none_stop=True)
