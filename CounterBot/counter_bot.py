import logging
import os

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler

from CounterBot import commands
from Database import user_dao
from models import User
from settings import TOKEN, APP_NAME, STATUS


def message_handler(bot, update):
    user = user_dao.get_user(update.effective_user.id)

    if user.status == STATUS.add_counter:
        commands.add_counter_process(bot, update)
    else:
        pass


def callback_handler(bot, update):
    user = user_dao.get_user(update.callback_query.message.chat.id)

    if user.status == STATUS.count:
        commands.count_process(bot, update, user)
    else:
        pass


def incoming_posts(update, context):
    pass
    # msg = update.message
    # if msg.forward_from_chat is not None:
    #     d = msg.date.strftime("%Y-%m-%dT%H:%M:%S")
    #     ch_username = ('@' + msg.forward_from_chat.username).lower()
    #     text = msg.text or msg.caption
    #
    #     message_dao.insert_message(msg.message_id, ch_username, msg.forward_from_message_id, d,
    #                                text)


def start_bot():
    port = os.environ.get('PORT', '8000')

    # Enable logging
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    logger = logging.getLogger(__name__)

    # Set up the Updater
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', commands.start))
    dp.add_handler(CommandHandler('add_counter', commands.add_counter))
    dp.add_handler(CommandHandler('count', commands.count))

    dp.add_handler(CallbackQueryHandler(callback_handler))
    dp.add_handler(MessageHandler(Filters.text, message_handler))

    # updater.start_webhook(listen="0.0.0.0",
    #                       port=int(port),
    #                       url_path=TOKEN)
    # updater.bot.setWebhook("https://{}.herokuapp.com/{}".format(APP_NAME, TOKEN))
    # updater.idle()

    updater.start_polling()
