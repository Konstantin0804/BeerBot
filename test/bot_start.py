# -*- coding: utf-8 -*-

from webtest import TestApp

from mbot_app.bm_app import app

chat_id = 1355819
# chat_id = 129058202

testApp = TestApp(app)


def test_start():
    testApp.post_json(
        '/HOOK',
        {"update_id": 490552167,
         "message": {
             "message_id": 22,
             "from": {
                 "id": chat_id, "first_name": "Stas",
                 "last_name": "Woronkow", "username": "svoronkov"},
             "chat": {
                 "id": chat_id,
                 "first_name": "Stas",
                 "last_name": "Woronkow",
                 "username": "svoronkov",
                 "type": "private"},
             "date": 163748865,
             "text": "/start",
             "entities": [{"type": "bot_command", "offset": 0, "length": 6}]
         }
         }
    )


def test_start_action_text():
    testApp.post_json(
        '/HOOK',
        {"update_id": 490552167,
         "message": {
             "message_id": 22,
             "from": {
                 "id": chat_id, "first_name": "Stas",
                 "last_name": "Woronkow", "username": "svoronkov"},
             "chat": {
                 "id": chat_id,
                 "first_name": "Stas",
                 "last_name": "Woronkow",
                 "username": "svoronkov",
                 "type": "private"},
             "date": 163748865,
             "text": "Пиво",
         }
         }
    )


def test_beer_action_text():
    testApp.post_json(
        '/HOOK',
        {"update_id": 490552167,
         "message": {
             "message_id": 22,
             "from": {
                 "id": chat_id, "first_name": "Stas",
                 "last_name": "Woronkow", "username": "svoronkov"},
             "chat": {
                 "id": chat_id,
                 "first_name": "Stas",
                 "last_name": "Woronkow",
                 "username": "svoronkov",
                 "type": "private"},
             "date": 163748865,
             "text": "Краны",
         }
         }
    )


def to_beers_root():
    testApp.post_json(
        '/HOOK',
        {"update_id": 490552167,
         "message": {
             "message_id": 22,
             "from": {
                 "id": chat_id, "first_name": "Stas",
                 "last_name": "Woronkow", "username": "svoronkov"},
             "chat": {
                 "id": chat_id,
                 "first_name": "Stas",
                 "last_name": "Woronkow",
                 "username": "svoronkov",
                 "type": "private"},
             "date": 163748865,
             "text": "К корню пива",
         }
         }
    )


def to_registration():
    testApp.post_json(
        '/HOOK',
        {"update_id": 490552167,
         "message": {
             "message_id": 22,
             "from": {
                 "id": chat_id, "first_name": "Stas",
                 "last_name": "Woronkow", "username": "svoronkov"},
             "chat": {
                 "id": chat_id,
                 "first_name": "Stas",
                 "last_name": "Woronkow",
                 "username": "svoronkov",
                 "type": "private"},
             "date": 163748865,
             "text": "Регистрация",
         }
         }
    )


def registration():
    testApp.post_json(
        '/HOOK',
        {"update_id": 490552167,
         "message": {
             "message_id": 22,
             "from": {
                 "id": chat_id, "first_name": "Stas",
                 "last_name": "Woronkow", "username": "svoronkov"},
             "chat": {
                 "id": chat_id,
                 "first_name": "Stas",
                 "last_name": "Woronkow",
                 "username": "svoronkov",
                 "type": "private"},
             "date": 163748865,
             "text": "Кремль 1",
         }
         }
    )


def to_begin():
    testApp.post_json(
        '/HOOK',
        {"update_id": 490552167,
         "message": {
             "message_id": 22,
             "from": {
                 "id": chat_id, "first_name": "Stas",
                 "last_name": "Woronkow", "username": "svoronkov"},
             "chat": {
                 "id": chat_id,
                 "first_name": "Stas",
                 "last_name": "Woronkow",
                 "username": "svoronkov",
                 "type": "private"},
             "date": 163748865,
             "text": "В начало",
         }
         }
    )


def reply_add():
    testApp.post_json(
        '/HOOK',
        {
            'update_id': 684932628,
            'callback_query': {
                'id': '5823202068026648',
                'from': {
                    'id': 1355819,
                    'is_bot': False,
                    'first_name': 'Stas',
                    'last_name': 'Woronkow',
                    'username': 'svoronkov',
                    'language_code': 'en'
                },
                'message': {
                    'message_id': 859,
                    'from': {
                        'id': 1233386930,
                        'is_bot': True,
                        'first_name': 'methodbeer_devandtest_bot',
                        'username': 'methodbeer_devandtest_bot'
                    },
                    'chat': {
                        'id': 1355819,
                        'first_name': 'Stas',
                        'last_name': 'Woronkow',
                        'username': 'svoronkov',
                        'type': 'private'
                    },
                    'date': 1587654516,
                    'photo': [
                        {
                            'file_id': 'AgACAgQAAxkDAAICEl6hvHJ16pQ99u1aVG7NV5KBPNzXAALkqjEbns20UDNh3U3CgfjATaO0GwAEAQADAgADbQADPH8FAAEYBA',
                            'file_unique_id': 'AQADTaO0GwAEPH8FAAE',
                            'file_size': 19661,
                            'width': 320,
                            'height': 319
                        },
                        {
                            'file_id': 'AgACAgQAAxkDAAICEl6hvHJ16pQ99u1aVG7NV5KBPNzXAALkqjEbns20UDNh3U3CgfjATaO0GwAEAQADAgADeAADPX8FAAEYBA',
                            'file_unique_id': 'AQADTaO0GwAEPX8FAAE',
                            'file_size': 48930,
                            'width': 500,
                            'height': 499
                        }
                    ],
                    'caption': 'Scratch (Zagovor Brewery) \n Stout - Oatmeal \n IBU: 30.0, ABV: 4.5 \n Цена: 280.00₽',
                    'caption_entities': [
                        {
                            'offset': 0,
                            'length': 7,
                            'type': 'bold'
                        },
                        {
                            'offset': 74,
                            'length': 7,
                            'type': 'bold'
                        }
                    ],
                    'reply_markup': {
                        'inline_keyboard': [
                            [
                                {
                                    'text': 'купить',
                                    'callback_data': 'add:19567378'
                                }
                            ]
                        ]
                    }
                },
                'chat_instance': '4804975644419024941',
                'data': 'add:19567378'
            }
        }
    )


def reply_remove():
    testApp.post_json(
        '/HOOK',
        {
            'update_id': 684932628,
            'callback_query': {
                'id': '5823202068026648',
                'from': {
                    'id': 1355819,
                    'is_bot': False,
                    'first_name': 'Stas',
                    'last_name': 'Woronkow',
                    'username': 'svoronkov',
                    'language_code': 'en'
                },
                'message': {
                    'message_id': 859,
                    'from': {
                        'id': 1233386930,
                        'is_bot': True,
                        'first_name': 'methodbeer_devandtest_bot',
                        'username': 'methodbeer_devandtest_bot'
                    },
                    'chat': {
                        'id': 1355819,
                        'first_name': 'Stas',
                        'last_name': 'Woronkow',
                        'username': 'svoronkov',
                        'type': 'private'
                    },
                    'date': 1587654516,
                    'photo': [
                        {
                            'file_id': 'AgACAgQAAxkDAAICEl6hvHJ16pQ99u1aVG7NV5KBPNzXAALkqjEbns20UDNh3U3CgfjATaO0GwAEAQADAgADbQADPH8FAAEYBA',
                            'file_unique_id': 'AQADTaO0GwAEPH8FAAE',
                            'file_size': 19661,
                            'width': 320,
                            'height': 319
                        },
                        {
                            'file_id': 'AgACAgQAAxkDAAICEl6hvHJ16pQ99u1aVG7NV5KBPNzXAALkqjEbns20UDNh3U3CgfjATaO0GwAEAQADAgADeAADPX8FAAEYBA',
                            'file_unique_id': 'AQADTaO0GwAEPX8FAAE',
                            'file_size': 48930,
                            'width': 500,
                            'height': 499
                        }
                    ],
                    'caption': 'Scratch (Zagovor Brewery) \n Stout - Oatmeal \n IBU: 30.0, ABV: 4.5 \n Цена: 280.00₽',
                    'caption_entities': [
                        {
                            'offset': 0,
                            'length': 7,
                            'type': 'bold'
                        },
                        {
                            'offset': 74,
                            'length': 7,
                            'type': 'bold'
                        }
                    ],
                    'reply_markup': {
                        'inline_keyboard': [
                            [
                                {
                                    'text': 'купить',
                                    'callback_data': 'add:19567378'
                                }
                            ]
                        ]
                    }
                },
                'chat_instance': '4804975644419024941',
                'data': 'remove:19567378'
            }
        }
    )


if __name__ == '__main__':
    #   test_start()
    #   test_beer_action_text()
    # reply_add()
    # reply_remove()
    # to_beers_root()
    # to_begin()
    to_registration()
    registration()
    test_beer_action_text()
