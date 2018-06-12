import os
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import Chat, Contact

def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Bem vindo ao " + bot.first_name + "!")

def echo(bot, update):
    user_name = update.message.chat['first_name'] + " " + update.message.chat['last_name']
    user_msg = update.message.text
    bot.send_message(chat_id=update.message.chat_id, text="Olá " + user_name + ", você enviou a mensagem: " + user_msg)

def unknown(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Desculpe, não entendi o comando:" + update.message.text)

def finish(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Atividades encerradas! Até mais...")
    updater.stop()                     

TOKEN=os.environ['TELEGRAM_TOKEN']
PORT = int(os.environ.get('PORT','8443'))

updater = Updater(TOKEN)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

dispatcher = updater.dispatcher

start_handler= CommandHandler('start', start)

dispatcher.add_handler(start_handler)

echo_handler = MessageHandler(Filters.text, echo)

dispatcher.add_handler(echo_handler)

unknown_handler = MessageHandler(Filters.text, unknown)

dispatcher.add_handler(unknown_handler)

finish_handler = CommandHandler('finish', finish)

dispatcher.add_handler(finish_handler)

if (__name__ == '__main__'):
    updater.start_webhook(listen='0.0.0.0',
                          port=PORT,
                          url_path=TOKEN)
    updater.bot.set_webhook('https://bot-borges.herokuapp.com/' + TOKEN)
    updater.idle()
    #updater.start_polling()


