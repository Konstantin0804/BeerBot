import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, \
    RegexHandler, ConversationHandler, CallbackQueryHandler
from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup, \
    InlineKeyboardButton, KeyboardButton, ReplyKeyboardRemove
from service.get_from_db import get_tap, get_bottle, \
    toggle_subscription, add_contact, add_address, add_to_cart, \
    delete_from_cart, checkout_cart, deactivate_cart, find_id, find_photo, cart_customer
import service.settings as settings

logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
                    )


def greet_user(bot, update, user_data):
    # print(user)
    text = 'Здравствуйте, {}'.format(update.message.chat.first_name)
    menu_keyboard = ReplyKeyboardMarkup([['Пиво', 'Корзина'], ['Регистрация', 'Инструцкии']], resize_keyboard=True, one_time_keyboard=True)
    update.message.reply_text(text, reply_markup=menu_keyboard)
    # TESTING ------------------------------------------------------
    # test_text = {"id": 20241496, "name": "Breakfast Basics", "style": "Sour - Fruited", "brewery": "Outline", "abv": "4.2", "ibu": "0.0", 
    # "label_image_hd": "https://beer.untappd.com/labels/3725269?size=hd", "position": 18, "price": "300.00", "c": 1}
    # update.message.reply_photo('https://beer.untappd.com/labels/3725269?size=hd', 'text')


def talk_to_me(bot, update, user_data):
    user_text = update.message.text
    print("А может ты "+user_text)
    update.message.reply_text("А может ты "+user_text+"?")


def beer(bot, update, user_data):
    text = 'Пиво'
    menu_keyboard = ReplyKeyboardMarkup([['Краны', 'Бутылки/Банки'], ['В начало']], resize_keyboard=True, one_time_keyboard=True)
    update.message.reply_text(text, reply_markup=menu_keyboard)


def taps(bot, update, user_data):
    text = get_tap()
    print(text)
    menu_keyboard = ReplyKeyboardMarkup([['К корню пива'],['Корзина']],[['В начало']], resize_keyboard=True, one_time_keyboard=True)
    add_keyboard = InlineKeyboardMarkup([[InlineKeyboardButton(text="Добавить", callback_data='1')]])
    for i in range(19):
        # update.message.reply_text(text[i], reply_markup=add_keyboard)
        # update.callback_query['caption_id'] = text[i]['id']
        # print(update)
        about = text[i]['name']+', Стиль: '+text[i]['style']+', Пивоварня: '+text[i]['brewery']+', ABV: '+text[i]['abv']+', IBU: '+text[i]['ibu']+'\n'+'Цена: '+text[i]['price']
        update.message.reply_photo(text[i]['label_image_hd'], about, reply_markup=add_keyboard)
    update.message.reply_text(reply_markup=menu_keyboard)


def add_button(bot, update, user_data):
    query = update.callback_query
    # print('add_button: ', query)
    if query.data == '1':
        t_id = find_id(query.message.caption, 'tap')
        c = add_to_cart(update.effective_user, t_id)

        add_keyboard = InlineKeyboardMarkup([[InlineKeyboardButton(text="Добавить ("+str(c)+')', callback_data='1'),
                                            InlineKeyboardButton(text="Убрать", callback_data='0')]])
        bot.edit_message_reply_markup(chat_id=query.message.chat.id, message_id=query.message.message_id, reply_markup=add_keyboard)
    elif query.data == '3':
        t_id = find_id(query.message.caption, 'bottle')
        # print(t_id)
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
    sect = list(text.values())[2:]
    styles = list()
    for i in sect:
        styles.append(i['bottle_name'])
        menu_keyboard = ReplyKeyboardMarkup([['/SALE', '/APA / IPA/ DIPA / PALE', '/STOUT / PORTER'],
                                        ['/SOUR / LAMBIC / SAISON / WILD / BRETT '],
                                        ['/FRUIT /BERRY / VEG', '/GERMAN WING', '/BELGIAN STYLE'],
                                        ['/BARLEYWINE / OLD / STRONG / WEE HEAVY', '/LAGER / KÖLSCH / HELLES / PILSNER'],
                                        ['/CIDER / MEAD', '/SOFT DRINKS / ALKO FREE'],
                                        ['К корню пива', 'Корзина', 'В начало']], resize_keyboard=True, one_time_keyboard=True)
    update.message.reply_text('Сорта пива в бутылках', reply_markup=menu_keyboard)


def bottles_section(bot, update, user_data):
    sect = get_bottles_section(update)
    text = get_bottle()
    text.pop('id')
    text.pop('name')
    k = ''
    menu_keyboard = ReplyKeyboardMarkup([['К разделам бутылок', 'Корзина'],['К корню пива', 'В начало']], resize_keyboard=True, one_time_keyboard=True)
    add_keyboard = InlineKeyboardMarkup([[InlineKeyboardButton(text="Добавить", callback_data='3')]])
    for i in text.values():
        k = i
        if i['bottle_name'][-1] == ' ':
            k['bottle_name'] = i['bottle_name'][:-1]
        if k['bottle_name'] == sect[1:]:
            k.pop("bottle_name")
            for j in k.values():
                # print(j)
                about = j['name']+', Стиль: '+j['style']+', Пивоварня: '+j['brewery']+', ABV: '+j['abv']+', IBU: '+j['ibu']+'\n'+'Цена: '+j['price']
                update.message.reply_photo(j['label_image_hd'],about, reply_markup=add_keyboard)
            break
    sect = ''
    text = ''
    update.message.reply_text(reply_markup=menu_keyboard)


def get_bottles_section(update):
    bottle_sect = update['message']['text']
    return bottle_sect



def registration(bot, update, user_data):
    text = 'Обозначьте себя'
    contact_button = KeyboardButton('Прислать контакты', request_contact=True)
    address_button = KeyboardButton('Ввести адрес доставки')
    menu_keyboard = ReplyKeyboardMarkup([[contact_button, address_button], ['В начало']], resize_keyboard=True, one_time_keyboard=True)
    update.message.reply_text(text, reply_markup=menu_keyboard)


def start_address(bot, update, user_data):
    update.message.reply_text("Введите адрес доставки", reply_markup=ReplyKeyboardRemove())
    return "address"


def cart(bot, update, user_data):
    cart = checkout_cart(update.effective_user, update.effective_user)
    menu_keyboard = ReplyKeyboardMarkup([['В начало', ' Заказать']], resize_keyboard=True, one_time_keyboard=True)
    #  print(cart)
    for i in cart.values():
        # print(i)
        cart_keyboard = InlineKeyboardMarkup([[InlineKeyboardButton(text="Добавить ("+str(i['c'])+')', callback_data='5'),
                                            InlineKeyboardButton(text="Убрать", callback_data='6')]])
        # update.message.reply_text(i, reply_markup=cart_keyboard)
        about = i['name']+', Стиль: '+i['style']+', Пивоварня: '+i['brewery']+', ABV: '+i['abv']+', IBU: '+i['ibu']+'\n'+'Цена: '+i['price']
        update.message.reply_photo(i['label_image_hd'], about, reply_markup= cart_keyboard)
    # update.message.reply_text('Chooooose', reply_markup=add_keyboard)
    update.message.reply_text('Ваш заказ', reply_markup=menu_keyboard)


def checkout(bot, update, user_data):
    cart = checkout_cart(update.effective_user, update.effective_user)
    customer = cart_customer(update.effective_user, update.effective_user)
    out = ''
    # print(cart)
    k = 0
    for i in cart.values():
        out = out + 'Наименование: '+str(i['name'])+', '+'количество: '+str(i['c'])+', '+'цена: '+str(i['price'])+', итого = '+str(int(i['c'])*float(i['price'])) + '\n'
        k = k + int(i['c'])*float(i['price'])
    out = out + '\n' + ' Итого: ' + str(k) + ' \n Заказчик: ' + str(customer['first_name'])+ ' '+ str(customer['last_name']) + ' ник: '+ str(customer['username']) + ' телефон: ' + str(customer['contacts']) + '\n адрес: ' + str(customer['address'])
    # print(k)
    # print(out)
    # print(customer['username'])
    if customer['contacts'] and customer['address']:
        bot.send_message(chat_id=129058202, text=out)
        deactivate_cart(update.effective_user, update.effective_user)
    else:
        menu_keyboard = ReplyKeyboardMarkup([['В начало', 'Регистрация']], resize_keyboard=True, one_time_keyboard=True)
        update.message.reply_text('Введите контактные данные по кнопке "Регистрация"', reply_markup=menu_keyboard)


def main():
    mybot = Updater(settings.API_KEY)
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user, pass_user_data=True))
    dp.add_handler(RegexHandler('^(Пиво)$', beer, pass_user_data=True))
    dp.add_handler(RegexHandler('^(Корзина)$', cart, pass_user_data=True))
    dp.add_handler(RegexHandler('^(Регистрация)$', registration, pass_user_data=True))
    dp.add_handler(RegexHandler('^(Краны)$', taps, pass_user_data=True))
    dp.add_handler(RegexHandler('^(Бутылки/Банки)$', bottles_root, pass_user_data=True))
    dp.add_handler(RegexHandler('^(В начало)$', greet_user, pass_user_data=True))
    dp.add_handler(RegexHandler('^(К корню пива)$', beer, pass_user_data=True))
    dp.add_handler(RegexHandler('^(Заказать)$', checkout, pass_user_data=True))
    dp.add_handler(RegexHandler('^(/)', bottles_section, pass_user_data=True))
    dp.add_handler(CallbackQueryHandler(add_button, pass_user_data=True))
    dp.add_handler(RegexHandler('^(К разделам бутылок)$', bottles_root, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me, pass_user_data=True))
    mybot.start_polling()
    mybot.idle()


if __name__ == "__main__":
    main()
