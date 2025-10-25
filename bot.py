from telebot import TeleBot
import cv2
import os
from logic import DB_Manager, create_collage
from config import DATABASE, TOKEN

bot = TeleBot(TOKEN)
db = DB_Manager(DATABASE)

@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(message.chat.id, "Привет! Я твой бот 🤖")

@bot.message_handler(commands=['my_score'])
def get_my_score(message):
    user_id = message.chat.id
    info = db.get_winners_img(user_id)
    prizes = [x[0] for x in info]

    all_images = os.listdir('img')
    image_paths = [f'img/{x}' if x in prizes else f'hidden_img/{x}' for x in all_images]

    collage = create_collage(image_paths)
    if collage is None:
        bot.send_message(message.chat.id, "У тебя пока нет призов 😔")
        return

    path = f'collages/collage_{user_id}.jpg'
    os.makedirs('collages', exist_ok=True)
    cv2.imwrite(path, collage)

    with open(path, 'rb') as photo:
        bot.send_photo(message.chat.id, photo, caption="Твой коллаж достижений 🏆")

if __name__ == "__main__":
    print("Бот запущен...")
    bot.infinity_polling()
