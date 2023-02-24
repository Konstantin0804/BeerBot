from datasource.db import db
from models import db_models


def get_tap():
    sections_tap = db.taps.find_one({'act_flg': 1})["menu"]["sections"][0]["items"]
    list_of_taps = []
    for section in sections_tap:
        single_tapitem = db_models.TapItem.from_dict(section).__dict__
        list_of_taps.append(single_tapitem)
    return list_of_taps


def get_bottle():
    sections_bottle = db.bottles.find_one({"act_flg": 1})["menu"]
    sections_bottle = db_models.Menu.from_dict(sections_bottle)
    bottles = dict()
    bottles['id'] = sections_bottle.id
    bottles['name'] = sections_bottle.name
    for i in range(len(sections_bottle.sections)):
        bottles[f'bottle_info_{i}'] = dict()
        i_item = sections_bottle.sections[i]
        bottles[f'bottle_info_{i}']['bottle_name'] = i_item.name
        for j in range(len(i_item.items)):
            j_item = i_item.items[j]
            if len(j_item.containers) > 0:
                bottles[f'bottle_info_{i}'][f'bottle_item_{j}'] = j_item.repr_necessary_data()
    return bottles


def get_bottle_names_dict(all_bottles):
    bottles_name_dict = {}
    for bottle, value in all_bottles.items():
        if bottle.startswith('bottle_info_') and len(value) > 1:
            bottles_name_dict[value.get('bottle_name')] = f"/{value.get('bottle_name')}"
    return bottles_name_dict


def add_address(user_data, address):
    print(address)
    db.users.update_one(
        {"_id": user_data["_id"]},
        {'$set': {'address': address}}
    )


def add_to_cart(user_id, beer_id):
    beer_id = str(beer_id)
    opened_cart = get_cart_by_user_id(user_id)
    if opened_cart:
        if not opened_cart.cart.get(beer_id):
            opened_cart.cart[beer_id] = 1
        else:
            opened_cart.cart[beer_id] += 1
        db.carts.update_one({'user_id': user_id.id, 'active_flag': 1},
                            {'$set': {'cart': opened_cart.cart}})
        count = opened_cart.cart.get(beer_id)
    else:
        new_cart = db_models.Cart(
            user_id=user_id.id,
            active_flag=1,
            cart={beer_id: 1}
        )
        db.carts.insert_one(new_cart.__dict__)
        count = 1
    return count


def delete_from_cart(user_id, beer_id):
    beer_id = str(beer_id)
    user_cart = get_cart_by_user_id(user_id)
    if user_cart:
        if not user_cart.cart.get(beer_id):
            return 0
        elif user_cart.cart.get(beer_id) > 1:
            user_cart.cart[beer_id] -= 1
            count = user_cart.cart[beer_id]
        else:
            user_cart.cart.pop(beer_id)
            count = 0
        db.carts.update_one({'user_id': user_id.id, 'active_flag': 1},
                            {'$set': {'cart': user_cart.cart}})
        return count


def get_cart_by_user_id(user_id):
    cart_dict = db.carts.find_one({'user_id': user_id.id, 'active_flag': 1})
    if not cart_dict:
        return None
    cart = db_models.Cart.from_dict(cart_dict)
    return cart


def find_user_is_registered(user_id):
    return db.users.find_one({'user_id': user_id})


def find_id(str_checkout, type_val):
    """
        Function for getting a beer ID from DB passing style and brewery.
        Not using now, artefact from previous versions, but may be useful in future
    """

    name = str_checkout.split(', Стиль: ')[0]
    brewery = str_checkout.split(', Стиль: ')[1].split(', Пивоварня: ')[1].split(', ABV')[0]
    # style = str_checkout.split('Стиль: ')[1].split(',')[0]
    if type_val == 'bottle':
        bottles = db.bottles.find_one({'act_flg': 1})
        bottle_menu = db_models.Menu(**bottles['menu'])
        found_beer = bottle_menu.find_beer_in_sections(name, brewery)
    else:
        taps = db.taps.find_one({'act_flg': 1})
        tap_menu = db_models.Menu(**taps['menu'])
        found_beer = tap_menu.find_tap_beer_in_sections(name, brewery)
    return found_beer


def checkout_cart(user_data):
    selected_cart = get_cart_by_user_id(user_data)
    if not selected_cart:
        return None
    taps = get_tap()
    bottles = get_bottle()
    checkout = dict()
    for j in selected_cart.cart:
        for i in taps:
            if i['id'] == int(j):
                checkout[i['id']] = i
                checkout[i['id']]['c'] = selected_cart.cart[j]
    bottles.pop('id')
    bottles.pop('name')
    for i in bottles.values():
        i.pop('bottle_name')
    for j in selected_cart.cart:
        for i in bottles.values():
            for k in i.values():
                if k['id'] == int(j):
                    checkout[k['id']] = k
                    checkout[k['id']]['c'] = selected_cart.cart[j]
    return checkout


def cart_customer(user_data, user_text):
    customer_data = db.users.find_one({'user_id': user_data['id']})
    return customer_data


def deactivate_cart(user_data):
    db.carts.update_one({'user_id': user_data['id'], 'active_flag': 1}, {'$set': {'active_flag': 0}})


if __name__ == '__main__':
    bottles = get_bottle()
    bottles_dict = get_bottle_names_dict(bottles)

