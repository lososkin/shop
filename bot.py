import telebot

bot = telebot.TeleBot('1255130676:AAEUrIBmfRVR04h4bGKnnKwHyuiQTeqYCnU')

@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    print(message.chat.id)


bot.polling()