import logging
from itertools import islice
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    RegexHandler,
    ConversationHandler,
    CallbackQueryHandler
)
from telegram import (
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    KeyboardButton
)
from service.get_from_db import (
    get_tap,
    get_bottle,
    add_to_cart,
    delete_from_cart,
    checkout_cart,
    deactivate_cart,
    find_user_is_registered,
    get_bottle_names_dict
)
from service.add_to_db import write_new_user, update_user_address
import service.settings as settings
import service.static_data as static_data
import service.message_constructors as message_constructors

logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
                    )


def greet_user(bot, update, user_data):
    menu_keyboard = ReplyKeyboardMarkup([['Пиво', 'Корзина'], ['Регистрация', 'Инструкции']],
                                        resize_keyboard=True, one_time_keyboard=True)
    update.message.reply_text(static_data.TALK_TO_ME.format(update.message.chat.first_name), reply_markup=menu_keyboard)


def instructions(bot, update, user_data):
    menu_keyboard = ReplyKeyboardMarkup([['Регистрация'], ['Пиво', 'В начало']],
                                        resize_keyboard=True, one_time_keyboard=True)
    update.message.reply_text(static_data.INSTRUCTIONS_TEXT, reply_markup=menu_keyboard)


def talk_to_me(bot, update, user_data):
    update.message.reply_text(static_data.MAYBE_YOU.format(update.message.text))


def beer(bot, update, user_data):
    text = 'Пиво'
    menu_keyboard = ReplyKeyboardMarkup([['Краны', 'Бутылки/Банки'], ['В начало']],
                                        resize_keyboard=True, one_time_keyboard=True)
    update.message.reply_text(text, reply_markup=menu_keyboard)


def taps(bot, update, user_data):
    text = get_tap()
    menu_keyboard = ReplyKeyboardMarkup(static_data.BUTTONS_ROOT_BUCKET_BEGIN,
                                        resize_keyboard=True, one_time_keyboard=True)
    for i in range(len(text)):
        callback_tap_data = f'add-{text[i]["id"]}'
        add_keyboard = InlineKeyboardMarkup([[InlineKeyboardButton(
            text="Добавить", callback_data=callback_tap_data)]])
        about = message_constructors.construct_tap_message(i, text)
        update.message.reply_photo(text[i]['label_image_hd'], about, reply_markup=add_keyboard)
    update.message.reply_text(reply_markup=menu_keyboard)


def add_button(bot, update, user_data):
    query = update.callback_query
    is_already_registered = find_user_is_registered(update.effective_user.id)
    if not is_already_registered:
        menu_keyboard = ReplyKeyboardMarkup(static_data.BUTTONS_REG_BEGIN, resize_keyboard=True, one_time_keyboard=True)
        update.message.reply_text(static_data.NOT_REGISTERED, reply_markup=menu_keyboard)
    else:
        callback_data = query.data.split('-')
        if callback_data[0] == 'add':
            c = add_to_cart(update.effective_user, callback_data[1])

            add_keyboard = InlineKeyboardMarkup([[InlineKeyboardButton(text="Добавить ("+str(c)+')', callback_data=f'add-{callback_data[1]}'),
                                                InlineKeyboardButton(text="Убрать", callback_data=f'del-{callback_data[1]}')]])
            bot.edit_message_reply_markup(chat_id=query.message.chat.id, message_id=query.message.message_id, reply_markup=add_keyboard)
        elif callback_data[0] == 'del':
            c = delete_from_cart(update.effective_user, callback_data[1])
            if c == 0:
                add_keyboard = InlineKeyboardMarkup([[InlineKeyboardButton(text="Добавить", callback_data=f'add-{callback_data[1]}')]])
                bot.edit_message_reply_markup(chat_id=query.message.chat.id, message_id=query.message.message_id, reply_markup=add_keyboard)
            else:
                add_keyboard = InlineKeyboardMarkup([[InlineKeyboardButton(text="Добавить ("+str(c)+')', callback_data=f'add-{callback_data[1]}'),
                                                InlineKeyboardButton(text="Убрать", callback_data=f'del-{callback_data[1]}')]])
                bot.edit_message_reply_markup(chat_id=query.message.chat.id, message_id=query.message.message_id, reply_markup=add_keyboard)


def bottles_root(bot, update, user_data):
    text = get_bottle()
    all_bottles_types = get_bottle_names_dict(text)
    if len(all_bottles_types) == 0:
        menu_keyboard = ReplyKeyboardMarkup(static_data.BUTTONS_ROOT_BUCKET_BEGIN, resize_keyboard=True,
                                            one_time_keyboard=True)
        update.message.reply_text(static_data.NO_BOTTLES_LEFT, reply_markup=menu_keyboard)
    else:
        keyboard_list = iter(all_bottles_types.values())
        keyboard_list_splitted = [list(islice(keyboard_list, elem)) for elem in
                                  settings.LENGTH_TO_SPLIT_BUTTONS_FOR_BOTTLE]
        menu_keyboard = ReplyKeyboardMarkup(keyboard_list_splitted + static_data.BUTTONS_ROOT_BUCKET_BEGIN,
                                            resize_keyboard=True, one_time_keyboard=True)
        update.message.reply_text(static_data.BEER_IN_BOTTLES, reply_markup=menu_keyboard)


def bottles_section(bot, update, user_data):
    sect = update.message.text
    text = get_bottle()
    text.pop('id')
    text.pop('name')
    menu_keyboard = ReplyKeyboardMarkup([['К разделам бутылок', 'Корзина'], ['К корню пива', 'В начало']],
                                        resize_keyboard=True, one_time_keyboard=True)
    for i in text.values():
        k = i
        if i['bottle_name'][-1] == ' ':
            k['bottle_name'] = i['bottle_name'][:-1]
        if k['bottle_name'] == sect[1:]:
            k.pop("bottle_name")
            for j in k.values():
                bottle_id = j['id']
                add_keyboard = InlineKeyboardMarkup([[InlineKeyboardButton(text="Добавить", callback_data=f'add-{bottle_id}')]])
                about = message_constructors.construct_cart_message(j)
                update.message.reply_photo(j['label_image_hd'], about, reply_markup=add_keyboard)
            break
    update.message.reply_text(reply_markup=menu_keyboard)


def registration(bot, update, user_data):
    is_already_registered = find_user_is_registered(update.effective_user.id)
    if not is_already_registered:
        contact_button = KeyboardButton(static_data.BUTTON_CONTACT, request_contact=True, one_time_keyboard=True)
        menu_keyboard = ReplyKeyboardMarkup([[contact_button], static_data.BUTTON_BEGIN[0]], resize_keyboard=True,
                                            one_time_keyboard=True)
        update.message.reply_text(static_data.TELL_ABOUT_YOU, reply_markup=menu_keyboard)
        return settings.NEW_USER
    else:
        address = is_already_registered.get('address')
        if not address:
            update.message.reply_text(static_data.ENTER_ADDRESS)
            return settings.ADD_ADDRESS
        else:
            menu_keyboard = ReplyKeyboardMarkup(static_data.BUTTON_BEGIN, resize_keyboard=True, one_time_keyboard=True)
    update.message.reply_text(static_data.ALREADY_REGISTERED, reply_markup=menu_keyboard)


def proceed_registration(bot, update, user_data):
    write_new_user(update.message)
    menu_keyboard = ReplyKeyboardMarkup(static_data.BUTTON_BEGIN, resize_keyboard=True, one_time_keyboard=True)
    update.message.reply_text(static_data.NEXT_ENTER_ADDRESS, reply_markup=menu_keyboard)
    return settings.ADD_ADDRESS


def start_address(bot, update, user_data):
    update_user_address(update)
    menu_keyboard = ReplyKeyboardMarkup(static_data.BUTTON_BEGIN, resize_keyboard=True, one_time_keyboard=True)
    update.message.reply_text(static_data.DONE, reply_markup=menu_keyboard)
    return ConversationHandler.END


def cart(bot, update, user_data):
    current_cart = checkout_cart(update.effective_user)
    if not current_cart:
        menu_keyboard = ReplyKeyboardMarkup(static_data.BUTTON_BEGIN, resize_keyboard=True, one_time_keyboard=True)
        update.message.reply_text(static_data.NO_ACTIVE_ORDERS, reply_markup=menu_keyboard)
    else:
        menu_keyboard = ReplyKeyboardMarkup([['В начало', ' Заказать']], resize_keyboard=True, one_time_keyboard=True)
        for i in current_cart.values():
            cart_keyboard = InlineKeyboardMarkup([[InlineKeyboardButton(
                text="Добавить ("+str(i['c'])+')', callback_data=f'add-{i["id"]}'),
                InlineKeyboardButton(text="Убрать", callback_data=f'del-{i["id"]}')]])
            about = message_constructors.construct_cart_message(i)
            update.message.reply_photo(i['label_image_hd'], about, reply_markup=cart_keyboard)
        update.message.reply_text('Ваш заказ', reply_markup=menu_keyboard)


def checkout(bot, update, user_data):
    cart_for_checkout = checkout_cart(update.effective_user)
    if not cart_for_checkout:
        menu_keyboard = ReplyKeyboardMarkup(static_data.BUTTON_BEGIN, resize_keyboard=True, one_time_keyboard=True)
        update.message.reply_text(static_data.NO_ACTIVE_ORDERS, reply_markup=menu_keyboard)
    else:
        customer = find_user_is_registered(update.effective_user.id)
        checkout_message = message_constructors.get_checkout_message(cart_for_checkout, customer)
        if customer['contacts'] and customer['address']:
            menu_keyboard = ReplyKeyboardMarkup(static_data.BUTTON_BEGIN, resize_keyboard=True, one_time_keyboard=True)
            update.message.reply_text(static_data.ORDER_PROCEEDED, reply_markup=menu_keyboard)
            bot.send_message(chat_id=int(settings.CHAT_FOR_CHECKOUT), text=checkout_message)
            deactivate_cart(update.effective_user)
        else:
            menu_keyboard = ReplyKeyboardMarkup(static_data.BUTTONS_REG_BEGIN, resize_keyboard=True,
                                                one_time_keyboard=True)
            update.message.reply_text(static_data.FINALY_ENTER_CONTACTS, reply_markup=menu_keyboard)


def main():
    registration_handler = ConversationHandler(
        entry_points=[RegexHandler('^(Регистрация)$', registration, pass_user_data=True)],
        states={
            settings.NEW_USER: [MessageHandler(Filters.contact, proceed_registration, pass_user_data=True)],
            settings.ADD_ADDRESS: [MessageHandler(Filters.text, start_address, pass_user_data=True)]
        },
        fallbacks=[RegexHandler('^(В начало)$', greet_user, pass_user_data=True)],
    )
    mybot = Updater(settings.API_KEY)
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user, pass_user_data=True))
    dp.add_handler(RegexHandler('^(Пиво)$', beer, pass_user_data=True))
    dp.add_handler(RegexHandler('^(Инструкции)$', instructions, pass_user_data=True))
    dp.add_handler(RegexHandler('^(Корзина)$', cart, pass_user_data=True))
    dp.add_handler(RegexHandler('^(Краны)$', taps, pass_user_data=True))
    dp.add_handler(RegexHandler('^(Бутылки/Банки)$', bottles_root, pass_user_data=True))
    dp.add_handler(RegexHandler('^(В начало)$', greet_user, pass_user_data=True))
    dp.add_handler(RegexHandler('^(К корню пива)$', beer, pass_user_data=True))
    dp.add_handler(RegexHandler('^(Заказать)$', checkout, pass_user_data=True))
    dp.add_handler(RegexHandler('^(/)', bottles_section, pass_user_data=True))
    dp.add_handler(CallbackQueryHandler(add_button, pass_user_data=True))
    dp.add_handler(RegexHandler('^(К разделам бутылок)$', bottles_root, pass_user_data=True))
    dp.add_handler(registration_handler)
    dp.add_handler(MessageHandler(Filters.text, talk_to_me, pass_user_data=True))
    mybot.start_polling()
    mybot.idle()


if __name__ == "__main__":
    main()
