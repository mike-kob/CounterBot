from telegram import InlineKeyboardMarkup, InlineKeyboardButton

from Database import user_dao, counter_dao
from models import User, Counter
from settings import STATUS


def start(bot, update):
    user = User(update.effective_user.id, update.effective_user.username)
    if not user_dao.user_exists(user):
        user_dao.save_user(user)
    bot.send_message(chat_id=user.user_id, text="Hello.\n/add_counter\n/count\n/edit", parse_mode='HTML')


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


def edit(bot, update, user=None):
    if user is None:
        user = User(update.effective_user.id, update.effective_user.username)
    user.change_status(STATUS.edit)
    user_dao.save_user(user)

    counters = counter_dao.get_user_counters(user)
    markup = InlineKeyboardMarkup(
        [[InlineKeyboardButton(counter.name + ': ' + str(counter.value), callback_data=counter.counter_id)] for counter
         in counters])
    bot.send_message(chat_id=user.user_id, text="Here's a list of your counters. Click on one you want to edit.",
                     reply_markup=markup,
                     parse_mode='HTML')


def edit_process(bot, update, user):
    counter_id = update.callback_query.data
    counter = counter_dao.get_counter(counter_id)
    counter_dao.save_current_counter(user, counter)
    user.change_status(STATUS.choose_edit_action)
    user_dao.save_user(user)

    markup = InlineKeyboardMarkup(
        [[InlineKeyboardButton('Rename', callback_data='Rename')],
         [InlineKeyboardButton('Set value', callback_data='Set value')],
         [InlineKeyboardButton('Delete', callback_data='Delete')]])
    bot.edit_message_text(chat_id=user.user_id, message_id=update.callback_query.message.message_id,
                          text='Counter:\n' + counter.name + ': ' + str(counter.value),
                          reply_markup=markup, parse_mode='HTML')


def choose_edit_process(bot, update, user):
    action = update.callback_query.data
    counter = counter_dao.get_current_counter(user)

    if action == 'Rename':
        pass
    elif action == 'Set value':
        pass
    elif action == 'Delete':
        markup = InlineKeyboardMarkup(
            [[InlineKeyboardButton('Yes', callback_data='Yes'),
              InlineKeyboardButton('Cancel', callback_data='Cancel')]])
        bot.edit_message_text(chat_id=user.user_id, message_id=update.callback_query.message.message_id,
                              text='Do you actually want to delete <b>"' +
                                   counter.name + '"</b> permanently?',
                              reply_markup=markup, parse_mode='HTML')
        user.change_status(STATUS.confirm_delete_action)
        user_dao.save_user(user)


def confirm_delete_process(bot, update, user):
    action = update.callback_query.data
    counter = counter_dao.get_current_counter(user)

    if action == 'Yes':
        counter_dao.delete_counter(counter)
        bot.edit_message_text(chat_id=user.user_id, message_id=update.callback_query.message.message_id,
                              text='Deleted',
                              reply_markup=None, parse_mode='HTML')
        edit(bot, update, user)
    elif action == 'Cancel':
        edit_process(bot, update, user)