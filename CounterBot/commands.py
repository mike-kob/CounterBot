from telegram import InlineKeyboardMarkup, InlineKeyboardButton

from Database import user_dao, counter_dao
from models import User, Counter
from settings import STATUS


def start(bot, update):
    user = User(update.effective_user.id, update.effective_user.username)
    if not user_dao.user_exists(user):
        user_dao.save_user(user)
    bot.send_message(chat_id=user.user_id, text="Hello.\n/add_counter\n/count", parse_mode='HTML')


def add_counter(bot, update):
    user = User(update.effective_user.id, update.effective_user.username)
    user.change_status(STATUS.add_counter)
    user_dao.save_user(user)
    bot.send_message(chat_id=user.user_id, text="OK. Send me a name for it", parse_mode='HTML')


def add_counter_process(bot, update):
    user = User(update.effective_user.id, update.effective_user.username, STATUS.add_counter)
    txt = update.effective_message.text
    counter = Counter(None, txt, user)
    counter_dao.save_counter(counter)
    bot.send_message(chat_id=user.user_id, text="OK. Saved", parse_mode='HTML')


def count(bot, update):
    user = User(update.effective_user.id, update.effective_user.username)
    user.change_status(STATUS.count)
    user_dao.save_user(user)
    counters = counter_dao.get_user_counters(user)
    markup = InlineKeyboardMarkup(
        [[InlineKeyboardButton(counter.name + ': ' + str(counter.value), callback_data=counter.counter_id)] for counter
         in counters])
    bot.send_message(chat_id=user.user_id, text="Click on counter to increment", reply_markup=markup, parse_mode='HTML')


def count_process(bot, update, user):
    counter_id = update.callback_query.data
    counter = counter_dao.get_counter(counter_id)
    counter.increment()
    counter_dao.save_counter(counter)

    counters = counter_dao.get_user_counters(user)
    markup = InlineKeyboardMarkup(
        [[InlineKeyboardButton(counter.name + ': ' + str(counter.value), callback_data=counter.counter_id)] for counter
         in counters])
    bot.edit_message_text(chat_id=user.user_id, message_id=update.callback_query.message.message_id,
                          text=update.callback_query.message.text,
                          reply_markup=markup, parse_mode='HTML')
