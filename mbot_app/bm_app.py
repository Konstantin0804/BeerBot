import os
import requests

from pprint import pprint
from werkzeug.middleware.shared_data import SharedDataMiddleware

from mbot_app.bm_bot import bot
from les13.wsgi.app import WSGIApplication

app = WSGIApplication(__name__)


@app.mapping(url='/set_webhook')
def set_webhook(**context):
    return requests.post(
        '{}{}'.format(bot.TELEGRAM_URL, 'setWebhook'),
        # TODO replace
        json={'url': 'https://methodbeerbot.herokuapp.com/HOOK'}
    )


@app.mapping(url='/HOOK')
def hook(**context):
    result = bot.dispatch(context)
    pprint(result)
    return 'ok'


@app.mapping(url='/status')
def simple_test(**context):
    return "status: up"


@app.mapping(url='/favicon.ico')
def favicon(**context):
    pass


if __name__ == '__main__':
    from werkzeug.serving import run_simple
    app = SharedDataMiddleware(app, {
        'info': os.path.join(os.path.dirname(__file__), 'static')
    })
    run_simple('127.0.0.1', 5000, app)
