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
    find_id,
    find_user_is_registered,
    get_bottle_names_dict
)
from service.add_to_db import write_new_user, update_user_address
import service.settings as settings

logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
                    )


def greet_user(bot, update, user_data):
    text = 'Здравствуйте, {}'.format(update.message.chat.first_name)
    menu_keyboard = ReplyKeyboardMarkup([['Пиво', 'Корзина'], ['Регистрация', 'Инструкции']],
                                        resize_keyboard=True, one_time_keyboard=True)
    update.message.reply_text(text, reply_markup=menu_keyboard)


def instructions(bot, update, user_data):
    text = 'Через меня можно заказать любимое пивко. \nСначала тебе нужно будет зарегистрироваться ' \
           '(это займет всего минуту), затем выбрать любимое пиво и оформить заказ. Такие дела.'
    menu_keyboard = ReplyKeyboardMarkup([['Регистрация'], ['Пиво', 'В начало']],
                                        resize_keyboard=True, one_time_keyboard=True)
    update.message.reply_text(text, reply_markup=menu_keyboard)


def talk_to_me(bot, update, user_data):
    user_text = update.message.text
    print("А может ты "+user_text)
    update.message.reply_text("А может ты "+user_text+"?")


def beer(bot, update, user_data):
    text = 'Пиво'
    menu_keyboard = ReplyKeyboardMarkup([['Краны', 'Бутылки/Банки'], ['В начало']],
                                        resize_keyboard=True, one_time_keyboard=True)
    update.message.reply_text(text, reply_markup=menu_keyboard)


def taps(bot, update, user_data):
    text = get_tap()
    menu_keyboard = ReplyKeyboardMarkup([['К корню пива', 'Корзина'], ['В начало']],
                                        resize_keyboard=True, one_time_keyboard=True)
    add_keyboard = InlineKeyboardMarkup([[InlineKeyboardButton(text="Добавить", callback_data='1')]])
    for i in range(len(text)):
        about = text[i]['name']+', Стиль: '+text[i]['style']+', Пивоварня: '+text[i]['brewery']+', ABV: '+text[i]['abv']+', IBU: '+text[i]['ibu']+'\n'+'Цена: '+text[i]['price']
        update.message.reply_photo(text[i]['label_image_hd'], about, reply_markup=add_keyboard)
    update.message.reply_text(reply_markup=menu_keyboard)


def add_button(bot, update, user_data):
    query = update.callback_query
    is_already_registered = find_user_is_registered(update.effective_user.id)
    if not is_already_registered:
        menu_keyboard = ReplyKeyboardMarkup([['В начало', 'Регистрация']], resize_keyboard=True, one_time_keyboard=True)
        update.message.reply_text('Кажется вы не зарегистрированы. Это займет всего 1 минуту, нажмите на Регистрация',
                                  reply_markup=menu_keyboard)
    else:
        if query.data == '1':
            t_id = find_id(query.message.caption, 'tap')
            c = add_to_cart(update.effective_user, t_id)

            add_keyboard = InlineKeyboardMarkup([[InlineKeyboardButton(text="Добавить ("+str(c)+')', callback_data='1'),
                                                InlineKeyboardButton(text="Убрать", callback_data='0')]])
            bot.edit_message_reply_markup(chat_id=query.message.chat.id, message_id=query.message.message_id, reply_markup=add_keyboard)
        elif query.data == '3':
            t_id = find_id(query.message.caption, 'bottle')
            c = add_to_cart(update.effective_user, t_id)
            add_keyboard = InlineKeyboardMarkup([[InlineKeyboardButton(text="Добавить ("+str(c)+')', callback_data='3'),
                                                InlineKeyboardButton(text="Убрать", callback_data='4')]])
            bot.edit_message_reply_markup(chat_id=query.message.chat.id, message_id=query.message.message_id, reply_markup=add_keyboard)
        elif query.data == '0':
            t_id = find_id(query.message.caption, 'tap')
            c = delete_from_cart(update.effective_user, t_id)
            if c == 0:
                add_keyboard = InlineKeyboardMarkup([[InlineKeyboardButton(text="Добавить", callback_data='1')]])
                bot.edit_message_reply_markup(chat_id=query.message.chat.id, message_id=query.message.message_id, reply_markup=add_keyboard)
            else:
                add_keyboard = InlineKeyboardMarkup([[InlineKeyboardButton(text="Добавить ("+str(c)+')', callback_data='1'),
                                                InlineKeyboardButton(text="Убрать", callback_data='0')]])
                bot.edit_message_reply_markup(chat_id=query.message.chat.id, message_id=query.message.message_id, reply_markup=add_keyboard)
        elif query.data == '4':
            t_id = find_id(query.message.caption, 'bottle')
            c = delete_from_cart(update.effective_user,  t_id)
            if c == 0:
                add_keyboard = InlineKeyboardMarkup([[InlineKeyboardButton(text="Добавить", callback_data='3')]])
                bot.edit_message_reply_markup(chat_id=query.message.chat.id, message_id=query.message.message_id, reply_markup=add_keyboard)
            else:
                add_keyboard = InlineKeyboardMarkup([[InlineKeyboardButton(text="Добавить ("+str(c)+')', callback_data='3'),
                                                InlineKeyboardButton(text="Убрать", callback_data='4')]])
                bot.edit_message_reply_markup(chat_id=query.message.chat.id, message_id=query.message.message_id, reply_markup=add_keyboard)
        elif query.data == '5' :
            t_id = find_id(query.message.caption, 'tap')
            if not t_id:
                t_id = find_id(query.message.caption, 'bottle')
            c = add_to_cart(update.effective_user, t_id)
            add_keyboard = InlineKeyboardMarkup([[InlineKeyboardButton(text="Добавить ("+str(c)+')', callback_data='5'),
                                                InlineKeyboardButton(text="Убрать", callback_data='6')]])
            bot.edit_message_reply_markup(chat_id=query.message.chat.id, message_id=query.message.message_id, reply_markup=add_keyboard)
        else:
            t_id = find_id(query.message.caption, 'tap')
            if not t_id:
                t_id = find_id(query.message.caption, 'bottle')
            c = delete_from_cart(update.effective_user, t_id)
            if c == 0:
                add_keyboard = InlineKeyboardMarkup([[InlineKeyboardButton(text="Добавить", callback_data='5')]])
                bot.edit_message_reply_markup(chat_id=query.message.chat.id, message_id=query.message.message_id, reply_markup=add_keyboard)
            else:
                add_keyboard = InlineKeyboardMarkup([[InlineKeyboardButton(text="Добавить ("+str(c)+')', callback_data='5'),
                                                InlineKeyboardButton(text="Убрать", callback_data='6')]])
                bot.edit_message_reply_markup(chat_id=query.message.chat.id, message_id=query.message.message_id, reply_markup=add_keyboard)


def bottles_root(bot, update, user_data):
    text = get_bottle()
    all_bottles_types = get_bottle_names_dict(text)
    if len(all_bottles_types) == 0:
        menu_keyboard = ReplyKeyboardMarkup([['К корню пива', 'Корзина'], ['В начало']],
                                            resize_keyboard=True, one_time_keyboard=True)
        update.message.reply_text('Кажется, на данный момент пива в бутылках не осталось', reply_markup=menu_keyboard)
    else:
        keyboard_list = iter(all_bottles_types.values())
        keyboard_list_splitted = [list(islice(keyboard_list, elem)) for elem in
                                  settings.LENGTH_TO_SPLIT_BUTTONS_FOR_BOTTLE]
        menu_keyboard = ReplyKeyboardMarkup(keyboard_list_splitted + [['К корню пива', 'Корзина', 'В начало']],
                                            resize_keyboard=True, one_time_keyboard=True)
        update.message.reply_text('Сорта пива в бутылках', reply_markup=menu_keyboard)


def bottles_section(bot, update, user_data):
    sect = update.message.text
    text = get_bottle()
    text.pop('id')
    text.pop('name')
    menu_keyboard = ReplyKeyboardMarkup([['К разделам бутылок', 'Корзина'], ['К корню пива', 'В начало']],
                                        resize_keyboard=True, one_time_keyboard=True)
    add_keyboard = InlineKeyboardMarkup([[InlineKeyboardButton(text="Добавить", callback_data='3')]])
    for i in text.values():
        k = i
        if i['bottle_name'][-1] == ' ':
            k['bottle_name'] = i['bottle_name'][:-1]
        if k['bottle_name'] == sect[1:]:
            k.pop("bottle_name")
            for j in k.values():
                about = j['name']+', Стиль: '+j['style']+', Пивоварня: '+j['brewery']+', ABV: '+j['abv']+', IBU: '+j['ibu']+'\n'+'Цена: '+j['price']
                update.message.reply_photo(j['label_image_hd'],about, reply_markup=add_keyboard)
            break
    update.message.reply_text(reply_markup=menu_keyboard)


def registration(bot, update, user_data):
    is_already_registered = find_user_is_registered(update.effective_user.id)
    if not is_already_registered:
        text = 'Обозначьте себя'
        contact_button = KeyboardButton('Прислать контакты', request_contact=True, one_time_keyboard=True)
        menu_keyboard = ReplyKeyboardMarkup([[contact_button], ['В начало']], resize_keyboard=True,
                                            one_time_keyboard=True)
        update.message.reply_text(text, reply_markup=menu_keyboard)
        return settings.NEW_USER
    else:
        address = is_already_registered.get('address')
        if not address:
            text = 'Вам нужно ввести адрес доставки:'
            update.message.reply_text(text)
            return settings.ADD_ADDRESS
        else:
            text = 'Вы уже зарегистрированы'
            menu_keyboard = ReplyKeyboardMarkup([['В начало']], resize_keyboard=True, one_time_keyboard=True)
    update.message.reply_text(text, reply_markup=menu_keyboard)


def proceed_registration(bot, update, user_data):
    text = 'Записал, спасибо. Теперь напишите адрес доставки:'
    write_new_user(update.message)
    menu_keyboard = ReplyKeyboardMarkup([['В начало']], resize_keyboard=True, one_time_keyboard=True)
    update.message.reply_text(text, reply_markup=menu_keyboard)
    return settings.ADD_ADDRESS


def start_address(bot, update, user_data):
    update_user_address(update)
    menu_keyboard = ReplyKeyboardMarkup([['В начало']], resize_keyboard=True, one_time_keyboard=True)
    update.message.reply_text('Готово!', reply_markup=menu_keyboard)
    return ConversationHandler.END


def cart(bot, update, user_data):
    current_cart = checkout_cart(update.effective_user)
    if not current_cart:
        menu_keyboard = ReplyKeyboardMarkup([['В начало']], resize_keyboard=True, one_time_keyboard=True)
        update.message.reply_text('У вас нет активных заказов.', reply_markup=menu_keyboard)
    else:
        menu_keyboard = ReplyKeyboardMarkup([['В начало', ' Заказать']], resize_keyboard=True, one_time_keyboard=True)
        for i in current_cart.values():
            cart_keyboard = InlineKeyboardMarkup([[InlineKeyboardButton(text="Добавить ("+str(i['c'])+')', callback_data='5'),
                                                InlineKeyboardButton(text="Убрать", callback_data='6')]])
            about = i['name']+', Стиль: '+i['style']+', Пивоварня: '+i['brewery']+', ABV: '+i['abv']+', IBU: '+i['ibu']+'\n'+'Цена: '+i['price']
            update.message.reply_photo(i['label_image_hd'], about, reply_markup= cart_keyboard)
        update.message.reply_text('Ваш заказ', reply_markup=menu_keyboard)


def checkout(bot, update, user_data):
    cart_for_checkout = checkout_cart(update.effective_user)
    if not cart_for_checkout:
        menu_keyboard = ReplyKeyboardMarkup([['В начало']], resize_keyboard=True, one_time_keyboard=True)
        update.message.reply_text('У вас нет активных заказов.', reply_markup=menu_keyboard)
    else:
        customer = find_user_is_registered(update.effective_user.id)
        out = 'Новый заказ:\n'
        k = 0
        for i in cart_for_checkout.values():
            if not i['price']:
                i['price'] = 0
            out = out + 'Наименование: '+str(i['name'])+', '+'количество: '+str(i['c'])+', '+'цена: '+str(i['price'])+', итого = '+str(int(i['c'])*float(i['price'])) + '\n'
            k = k + int(i['c'])*float(i['price'])
        out = out + '\n' + 'Итого: ' + str(k) + '\n Заказчик: ' + str(customer['first_name'])+ ' '+ str(customer['last_name']) + '\n ник: '+ str(customer['username']) + '\n телефон: ' + str(customer['contacts']) + '\n адрес: ' + str(customer['address'])
        if customer['contacts'] and customer['address']:
            menu_keyboard = ReplyKeyboardMarkup([['В начало']], resize_keyboard=True, one_time_keyboard=True)
            update.message.reply_text('Ваш заказ отправлен, скоро с вами свяжутся', reply_markup=menu_keyboard)
            bot.send_message(chat_id=int(settings.CHAT_FOR_CHECKOUT), text=out)
            deactivate_cart(update.effective_user)
        else:
            menu_keyboard = ReplyKeyboardMarkup([['В начало', 'Регистрация']], resize_keyboard=True,
                                                one_time_keyboard=True)
            update.message.reply_text('Введите контактные данные по кнопке "Регистрация"', reply_markup=menu_keyboard)


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
