import requests
from settings import HEADERS
from mbot_app.datasource.db import db
from mbot_app.models import db_models


def tap_list():
    pos_tap_url = "https://business.untappd.com/api/v1/menus/81847?full=true"
    result_pos_tap = requests.get(pos_tap_url, headers=HEADERS)
    tap = result_pos_tap.json()
    return db_models.Tap(**tap)


def bottle_list():
    pos_bottle_url = "https://business.untappd.com/api/v1/menus/94668?full=true"
    result_pos_bottle = requests.get(pos_bottle_url, headers=HEADERS)
    bottle = result_pos_bottle.json()
    return db_models.Tap(**bottle)


def add_tap(tap):
    db.taps.update_many({'act_flg': 1}, {'$set': {"act_flg": 0}})
    db.taps.insert_one(tap.__dict__)


def add_bottle(bottle):
    db.bottles.update_many({'act_flg': 1}, {'$set': {"act_flg": 0}})
    db.bottles.insert_one(bottle.__dict__)


if __name__ == '__main__':
    add_tap(tap_list())
    add_bottle(bottle_list())
