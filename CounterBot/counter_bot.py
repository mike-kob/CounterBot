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
    elif user.status == STATUS.edit:
        commands.edit_process(bot, update, user)
    elif user.status == STATUS.choose_edit_action:
        commands.choose_edit_process(bot, update, user)
    elif user.status == STATUS.confirm_delete_action:
        commands.confirm_delete_process(bot, update, user)
    else:
        pass


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
    dp.add_handler(CommandHandler('edit', commands.edit))

    dp.add_handler(CallbackQueryHandler(callback_handler))
    dp.add_handler(MessageHandler(Filters.text, message_handler))
    #
    # updater.start_webhook(listen="0.0.0.0",
    #                       port=int(port),
    #                       url_path=TOKEN)
    # updater.bot.setWebhook("https://{}.herokuapp.com/{}".format(APP_NAME, TOKEN))
    # updater.idle()

    updater.start_polling()
