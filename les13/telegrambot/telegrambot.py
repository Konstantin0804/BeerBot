import requests

BASE_TELEGRAM_URL = 'https://api.telegram.org/bot'
SEND_MESSAGE_SUFFIX = 'sendMessage'
SEND_VENUE_SUFFIX = 'sendVenue'
SEND_PHOTO_SUFFIX = 'sendPhoto'
SEND_CHAT_ACTION_SUFFIX = 'sendChatAction'
EDIT_MESSAGE_TEXT_SUFFIX = 'editMessageText'
EDIT_MESSAGE_REPLY_MARKUP_SUFFIX = 'editMessageReplyMarkup'
GET_CHAT_SUFFIX = 'getChat'

proxies = {
    'https': 'socks5://learn:python@t1.learn.python.ru:1080',
}


def url(*args):
    return ''.join(args)


class TelegramBot(object):
    actions = {}
    text_actions = {}
    callback_actions = {}
    state_getter = None

    def __init__(self, token):
        self.commands = {}
        self.token = token
        self.TELEGRAM_URL = url(BASE_TELEGRAM_URL, self.token, '/')

    def state_getter(self, **options):
        def decorator(f):
            self.state_getter = f
            print('add state getter with {}'.format(options))
            return f
        return decorator

    def action(self, action_type=None, **options):
        def decorator(f):
            self.actions[action_type] = f
            print('add {} with {}'.format(action_type, options))
            return f

        return decorator

    def text_action(self, text_action=None, **options):
        def decorator(f):
            self.text_actions[text_action] = f
            print('add {} with {}'.format(text_action, options))
            return f

        return decorator

    def callback_action(self, callback_action=None, **options):
        def decorator(f):
            self.callback_actions[callback_action] = f
            print('add {} with {}'.format(callback_action, options))
            return f

        return decorator

    def dispatch(self, context):
        data = context.get('data') or {}
        message = data.get('message', {})
        text = message.get('text')

        print('CONTEXT DATA: {}'.format(context.get('data')))

        if 'location' in message:
            self.actions['location'](context)
        elif 'callback_query' in data:
            data_context_raw = data['callback_query']['data']
            data_context = data_context_raw.split(":")
            action = data_context[0]
            self.callback_actions[action](context)
        elif 'entities' in message:
            for entity in message.get('entities', []):
                if entity['type'] == 'bot_command':
                    bot_command = text[entity['offset']:entity['length']]
                    try:
                        self.actions[bot_command](context)
                    except Exception as e:
                        print(e)
        else:
            text_action = text
            state = self.state_getter()
            try:
                if state is not None:
                    chat_id = context.get('data')['message']['chat']['id']
                    action = None
                    if str(chat_id) in state:
                        action = state[str(chat_id)]
                    if action is not None:
                        action(context)
                    else:
                        self.text_actions[text_action](context)
            except Exception as e:
                print(e)

    def send_message(self, chat_id=None, text=None, reply_markup=None):
        data = {
            'chat_id': chat_id,
            'text': text
        }

        if reply_markup:
            data['reply_markup'] = reply_markup

        return requests.get(
            url(self.TELEGRAM_URL, SEND_MESSAGE_SUFFIX),
            json=data,
            proxies=proxies
        )

    def send_photo(self, chat_id=None, caption=None, photo=None, parse_mode=None, reply_markup=None):
        data = {
            'chat_id': chat_id,
            'photo': photo,
            'caption': caption
        }

        if reply_markup:
            data['reply_markup'] = reply_markup

        if parse_mode:
            data['parse_mode'] = parse_mode

        return requests.get(
            url(self.TELEGRAM_URL, SEND_PHOTO_SUFFIX),
            json=data,
            proxies=proxies
        )

    def send_chat_action(self, chat_id=None, action=None):
        return requests.post(
            url(self.TELEGRAM_URL, SEND_CHAT_ACTION_SUFFIX),
            json={'chat_id': chat_id, 'action': action}
        )

    def get_chat(self, chat_id=None):
        return requests.post(
            url(self.TELEGRAM_URL, GET_CHAT_SUFFIX),
            json={'chat_id': chat_id}
        )

    def send_venue(self, chat_id=None, text=None, title=None,
                   caption=None, address=None, latitude=None,
                   longitude=None):
        return requests.post(
            url(self.TELEGRAM_URL, SEND_VENUE_SUFFIX),
            json={
                'chat_id': chat_id,
                'text': text,
                'caption': caption,
                'latitude': latitude,
                'longitude': longitude,
                'title': title,
                'address': address
            }
        )

    def edit_message_text(self, chat_id=None, message_id=None, text=None, reply_markup=None):
        data = {
            'chat_id': chat_id,
            'message_id': message_id,
            'text': text
        }

        if reply_markup:
            data['reply_markup'] = reply_markup

        return requests.post(
            url(self.TELEGRAM_URL, EDIT_MESSAGE_TEXT_SUFFIX),
            json=data
        )

    def edit_message_reply_markup(self, chat_id=None, message_id=None, reply_markup=None):
        data = {
            'chat_id': chat_id,
            'message_id': message_id,
            'reply_markup': reply_markup
        }

        return requests.post(
            url(self.TELEGRAM_URL, EDIT_MESSAGE_REPLY_MARKUP_SUFFIX),
            json=data
        )
