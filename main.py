import telebot

from MessageHandler import UserMessageHandler

bot = telebot.TeleBot("Token")

@bot.message_handler(commands=['start'])
def start_message(message):
	bot.send_message(message.chat.id,"Здравствуй. Я рад! Ты разговариваешь со мной")

@bot.message_handler(content_types=['text'])
def send_welcome(message):
	sentence = message.text.lower()
	bot.send_message(message.chat.id, UserMessageHandler.handle(sentence))

bot.polling()
