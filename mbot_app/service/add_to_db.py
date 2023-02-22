import requests
from mbot_app.service.settings import HEADERS, TAP_URL, BOTTLE_URL
from mbot_app.datasource.db import db
from mbot_app.models import db_models


def tap_list():
    pos_tap_url = TAP_URL
    result_pos_tap = requests.get(pos_tap_url, headers=HEADERS)
    tap = result_pos_tap.json()
    return db_models.Tap(**tap)


def bottle_list():
    pos_bottle_url = BOTTLE_URL
    result_pos_bottle = requests.get(pos_bottle_url, headers=HEADERS)
    bottle = result_pos_bottle.json()
    return db_models.Tap(**bottle)


def add_tap(tap):
    db.taps.update_many({'act_flg': 1}, {'$set': {"act_flg": 0}})
    db.taps.insert_one(tap.__dict__)


def add_bottle(bottle):
    db.bottles.update_many({'act_flg': 1}, {'$set': {"act_flg": 0}})
    db.bottles.insert_one(bottle.__dict__)


def write_new_user(user):
    user_data = db_models.User(
        user_id=user.effective_attachment.user_id,
        username=user.chat.username,
        chat_id=user.chat.id,
        first_name=user.effective_attachment.first_name,
        last_name=user.effective_attachment.last_name,
        contacts=user.effective_attachment.phone_number
    )
    db.users.insert_one(user_data.__dict__)


def update_user_address(message_data):
    address = message_data.message.text
    user_id = message_data.effective_user.id
    db.users.update_one({'user_id': user_id}, {'$set': {'address': address}})


if __name__ == '__main__':
    add_tap(tap_list())
    add_bottle(bottle_list())
