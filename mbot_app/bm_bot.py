# -*- coding: utf-8 -*-

from les13.telegrambot.telegrambot import TelegramBot
from keyboard.keyboards import KEYBOARD_START, KEYBOARD_BEER, KEYBOARD_TAP, KEYBOARD_REGISTRATION
from service.get_from_db import get_tap, add_to_cart, delete_from_cart, user_put_if_absent, add_address
import logging

logger = logging.getLogger(__name__)

# TODO replace
bot = TelegramBot('1233386930:AAHZ-zOVS3EMEalUpvkX8ELZ6tEOhSjf6ho')

STATE = {}

ACTION_ADD_TAP = 'add-tap'
ACTION_REMOVE_TAP = 'remove-tap'


@bot.state_getter()
def state_getter():
    return STATE


@bot.action(action_type='/start')
def start_action(context):
    start(context)


@bot.text_action(text_action='В начало')
def start_menu(context):
    start(context)


def start(context):
    try:
        chat_id = context.get('data')['message']['chat']['id']
        print(bot.send_message(
            chat_id=chat_id,
            text='start',
            reply_markup=KEYBOARD_START
        ).content)
    except Exception as e:
        print(e)


@bot.text_action(text_action='Пиво')
def beer_menu(context):
    beer(context)


@bot.text_action(text_action='К корню пива')
def beer_menu_back(context):
    beer(context)


@bot.text_action(text_action='Регистрация')
def registration_menu(context):
    try:
        chat_id = context.get('data')['message']['chat']['id']
        print(bot.send_message(
            chat_id=chat_id,
            text='Обозначьте себя',
            reply_markup=KEYBOARD_REGISTRATION
        ).content)
        STATE[str(chat_id)] = registration
    except Exception as e:
        print(e)


def registration(context):
    message = context.get('data')['message']
    chat_id = message['chat']['id']
    text = message['text']
    user = message['from']
    user = user_put_if_absent(user, chat_id)
    if text:
        add_address(user, text)
        STATE[str(chat_id)] = None
        print(bot.send_message(
            chat_id=chat_id,
            text='Спасибо',
            reply_markup=KEYBOARD_START
        ).content)
    else:
        print(bot.send_message(
            chat_id=chat_id,
            text='Введите хоть что-нибудь'
        ).content)
    print("user: {}".format(user))


def beer(context):
    try:
        chat_id = context.get('data')['message']['chat']['id']
        print(bot.send_message(
            chat_id=chat_id,
            text='Пиво',
            reply_markup=KEYBOARD_BEER
        ).content)
    except Exception as e:
        print(e)


@bot.text_action(text_action='Краны')
def taps_menu(context):
    try:
        chat_id = context.get('data')['message']['chat']['id']
        taps = get_tap()
        print(bot.send_message(
            chat_id=chat_id,
            text='Краны',
            reply_markup=KEYBOARD_TAP
        ).content)
        for tapNumber in taps:
            tap = taps[tapNumber]
            text = '*{}* ({}) \r\n {} \r\n IBU: {}, ABV: {} \r\n Цена: *{}₽*'.format(tap['name'], tap['brewery'],
                                                                                     tap['style'], tap['ibu'],
                                                                                     tap['abv'], tap['price'])
            print(text)
            print(bot.send_photo(
                chat_id=chat_id,
                caption=text,
                photo=tap['label_image_hd'],
                parse_mode='Markdown',
                reply_markup={
                    'inline_keyboard': [[{'text': 'Добавить', 'callback_data':  ACTION_ADD_TAP + ':'+str(tap['id'])}]]
                }
            ).content)
    except Exception as e:
        print(e)


@bot.callback_action(callback_action=ACTION_ADD_TAP)
def add_beer(context):
    try:
        message_id, chat_id, beer_id, user_id = prepare_callback_context(context)
        print(beer_id)
        count = add_to_cart(user_id, beer_id)
        print(bot.edit_message_reply_markup(
            chat_id=chat_id,
            message_id=message_id,
            reply_markup=prepare_change_cart_reply_markup(count, beer_id)
        ).content)
    except Exception as e:
        print(e)


@bot.callback_action(callback_action=ACTION_REMOVE_TAP)
def remove_beer(context):
    try:
        message_id, chat_id, beer_id, user_id = prepare_callback_context(context)
        count = delete_from_cart(user_id, beer_id)
        print(bot.edit_message_reply_markup(
            chat_id=chat_id,
            message_id=message_id,
            reply_markup=prepare_change_cart_reply_markup(count, beer_id)
        ).content)
    except Exception as e:
        print(e)


def prepare_callback_context(context):
    query = context.get('data')['callback_query']
    message_id = query['message']['message_id']
    chat_id = query['message']['chat']['id']
    beer_id = query['data'].split(':')[1]
    user_id = query['from']['id']
    return message_id, chat_id, beer_id, user_id


def prepare_change_cart_reply_markup(count, beer_id):
    if count > 0:
        reply_markup = {
            'inline_keyboard': [
                [{'text': 'Добавить (' + str(count) + ')', 'callback_data': ACTION_ADD_TAP + ':' + str(beer_id)}],
                [{'text': 'Убрать', 'callback_data':  ACTION_REMOVE_TAP + ':' + str(beer_id)}]
            ]
        }
    else:
        reply_markup = {
            'inline_keyboard': [
                [{'text': 'Добавить', 'callback_data':  ACTION_ADD_TAP + ':' + str(beer_id)}]
            ]
        }
    return reply_markup
