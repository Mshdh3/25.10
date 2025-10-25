from telebot import TeleBot, types
from logiт import DB_Manager
from config import DATABASE, TOKEN  

bot = TeleBot(TOKEN)
db = DB_Manager(DATABASE)

@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(message.chat.id, "Привет! Я твой бот 🤖")


@bot.message_handler(commands=['rating'])
def handle_rating(message):
    res = db.get_rating()
    if not res:
        bot.send_message(message.chat.id, "Пока нет данных о победителях 🕓")
        return

    table_rows = [f'| @{x[0]:<11} | {x[1]:<11}|\n{"_"*26}' for x in res]
    result = '\n'.join(table_rows)
    header = f'|USER_NAME    |COUNT_PRIZE|\n{"_"*26}\n'
    bot.send_message(message.chat.id, header + result)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    prize_id = call.data
    user_id = call.message.chat.id

    # Проверяем, сколько победителей уже есть
    winners_count = db.get_winners_count(prize_id)

    if winners_count < 3:
        # Добавляем победителя (пример, зависит от реализации в твоей БД)
        res = db.add_winner(user_id, prize_id)
        if res:
            img = db.get_prize_image(prize_id)
            with open(f'img/{img}', 'rb') as photo:
                bot.send_photo(user_id, photo, caption="🎉 Поздравляем! Ты получил картинку!")
        else:
            bot.send_message(user_id, "Ты уже получил этот приз!")
    else:
        bot.send_message(user_id, "😔 К сожалению, призы уже разобрали. Попробуй в следующий раз!")

if __name__ == "__main__":
    print("Бот запущен...")
    bot.infinity_polling()
