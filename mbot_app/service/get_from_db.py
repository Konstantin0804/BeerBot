from mbot_app.datasource.db import db
from mbot_app.models import db_models


def get_tap():
    sections_tap = db.taps.find_one({'act_flg': 1})["menu"]["sections"][0]["items"]
    list_of_taps = []
    for section in sections_tap:
        single_tapitem = db_models.TapItem.from_dict(section).__dict__
        list_of_taps.append(single_tapitem)
    return list_of_taps


def get_bottle():
    sections_bottle = db.bottles.find_one({"act_flg": 1})
    ks = ['id', 'name', 'style', 'brewery', 'abv', 'ibu', 'label_image_hd']
    bottles = dict()
    bottles['id'] = sections_bottle['menu']['id']
    bottles['name'] = sections_bottle['menu']['name']
    for i in range(len(sections_bottle['menu']['sections'])):
        bottles[f'bottle_info_{i}'] = dict()
        i_item = sections_bottle['menu']['sections'][i]
        bottles[f'bottle_info_{i}']['bottle_name'] = i_item['name']
        for j in range(len(i_item['items'])):
            j_item = i_item['items'][j]
            # print(j_item.keys())
            bottles[f'bottle_info_{i}'][f'bottle_item_{j}'] = {key: j_item[key] for key in ks }
            bottles[f'bottle_info_{i}'][f'bottle_item_{j}']['price'] = j_item['containers'][0]['price']
            # bottles[f'bottle_info_{i}'][f'bottle_item'] = {key: j_item[key] for key in ks }
    return bottles


def user_put_if_absent(user_candidate, chat_id):
    user = db.users.find_one({"user_id": user_candidate['id']})
    if not user:
        user = {
            "user_id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "username": user.username,
            "chat_id": user.chat_id
        }
        db.users.insert_one(user)
    return user


def toggle_subscription(user_data):
    if not user_data.get("subscribed"):
        user_data['subscribed'] = True
    else:
        user_data['subscribed'] = False
    db.users.update_one(
        {"_id": user_data["_id"]},
        {'$set': {'subscribed': user_data['subscribed']}}
    )


def add_contact(user_data, message):
    # print(user_data)
    # print(message.contact.phone_number)
    # print(db.users.find_one({"_id": user_data["_id"]}))
    db.users.update_one(
        {"_id": user_data["_id"]},
        {'$set': {'contacts': message.contact.phone_number}}
    )


def add_address(user_data, address):
    print(address)
    db.users.update_one(
        {"_id": user_data["_id"]},
        {'$set': {'address': address}}
    )


def add_to_cart(user_id, beer_id):
    beer_id = str(beer_id)
    if db.carts.find_one({'user_id': user_id, 'active_flag': 1}):
        user_cart = get_cart_by_user_id(user_id)
        user_cart[beer_id] = user_cart.get(beer_id, 0) + 1
        db.carts.update_one({'user_id': user_id, 'active_flag': 1}, {'$set': {'cart': user_cart}})
        count = user_cart.get(beer_id)
    else:
        db.carts.insert_one({'user_id': user_id, 'active_flag': 1, 'cart': {beer_id: 1}})
        count = 1
    return count


def delete_from_cart(user_id, beer_id):
    beer_id = str(beer_id)
    user_cart = get_cart_by_user_id(user_id)
    user_cart[beer_id] = user_cart.get(beer_id, 0) - 1
    db.carts.update_one({'user_id': user_id, 'active_flag': 1}, {'$set': {'cart': user_cart}})
    count = user_cart.get(beer_id, 0)
    return count


def get_cart_by_user_id(user_id=None):
    return db.carts.find_one({'user_id': user_id, 'active_flag': 1})['cart']


def find_id(str_checkout, type_val):
    # print('find ',str_checkout)
    # print('find ',type_val)
    taps = db.taps.find_one({'act_flg':1})
    bottles = db.bottles.find_one({'act_flg':1})
    # print('bottles: ', bottles)
    name = str_checkout.split(', Стиль: ')[0]
    brewery = str_checkout.split(', Стиль: ')[1].split(', Пивоварня: ')[1].split(', ABV')[0]
    style = str_checkout.split('Стиль: ')[1].split(',')[0]
    tap_id = ''
    bot_id = ''
    if type_val == 'tap':
        for i in taps['menu']['sections'][0]['items']:
            # print(i['name'])
            if i['name'] == name and i['brewery'] == brewery:
                tap_id = i['id']
        return tap_id
    else:
        # print('sectionssss:   ', bottles['menu']['sections'])
        for i in bottles['menu']['sections']:
            for j in i['items']:
                if j['name'] == name and j['brewery'] == brewery:
                    bot_id = j['id']
        return bot_id


def find_photo(str_checkout, type_val):
    # print('find ',str_checkout)
    # print('find ',type_val)
    taps = db.taps.find_one({'act_flg':1})
    bottles = db.bottles.find_one({'act_flg':1})
    name = str_checkout.split(', Стиль: ')[0]
    brewery = str_checkout.split(', Стиль: ')[1].split(', Пивоварня: ')[1].split(', ABV')[0]
    style = str_checkout.split('Стиль: ')[1].split(',')[0]
    tap_id = ''
    bot_id = ''
    if type_val == 'tap':
        for i in taps['menu']['sections'][0]['items']:
            # print(i['name'])
            if i['name'] == name and i['brewery'] == brewery:
                photo = i['label_image_hd']
        return photo
    else:
        for i in bottles['menu']['sections']:
            if i['name'] == style:
                for j in i['items']:
                    if j['name'] == name and j['brewery'] == brewery:
                        photo = j['label_image_hd']
        return photo


def checkout_cart(user_data, user_text):
    current_cart = db.carts.find_one({'user_id': user_data['id'], 'active_flag':1})
    # print(customer_data)
    taps = get_tap()
    bottles = get_bottle()
    # print(taps)
    checkout = dict()
    for j in current_cart['cart']:
        for i in taps.values():
            if i['id'] == int(j):
                checkout[i['id']] = i
                checkout[i['id']]['c'] = current_cart['cart'][j]
    bottles.pop('id')
    bottles.pop('name')
    for i in bottles.values():
        i.pop('bottle_name')
    for j in current_cart['cart']:
        for i in bottles.values():
            for k in i.values():
                if k['id'] == int(j):
                    checkout[k['id']] = k
                    checkout[k['id']]['c'] = current_cart['cart'][j]
    return checkout


def cart_customer(user_data, user_text):
    customer_data = db.users.find_one({'user_id': user_data['id']})
    return customer_data


def deactivate_cart(user_data, user_text):
    db.carts.update_one({'user_id': user_data['id'],'active_flag': 1},{'$set': {'active_flag' :0}})


if __name__ == '__main__':
    get_tap()
