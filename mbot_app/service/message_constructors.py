def construct_cart_message(item):
    return item['name'] + ', Стиль: ' + item['style'] + ', Пивоварня: ' + item['brewery'] + ', ABV: ' \
        + item['abv'] + ', IBU: ' + item['ibu'] + '\n' + 'Цена: ' + item['price']


def construct_checkout_message(checkout_item):
    return 'Наименование: ' + str(checkout_item['name']) + ', ' + 'количество: ' + str(checkout_item['c']) + ', ' \
        + 'цена: ' + str(checkout_item['price']) + ', итого = ' + str(
            int(checkout_item['c']) * float(checkout_item['price'])) + '\n'


def construct_final_checkout_message(price, customer):
    return '\n' + 'Итого: ' + str(price) + '\n Заказчик: ' + str(customer['first_name']) + ' ' + str(
        customer['last_name']) + '\n ник: ' + str(customer['username']) + '\n телефон: ' + str(
        customer['contacts']) + '\n адрес: ' + str(customer['address'])


def construct_tap_message(i, text):
    return text[i]['name'] + ', Стиль: ' + text[i]['style'] + ', Пивоварня: ' + text[i]['brewery'] + ', ABV: ' + \
        text[i][
            'abv'] + ', IBU: ' + text[i]['ibu'] + '\n' + 'Цена: ' + text[i]['price']


def get_checkout_message(cart_for_checkout, customer):
    out = 'Новый заказ:\n'
    k = 0
    for i in cart_for_checkout.values():
        if not i['price']:
            i['price'] = 0
        out = out + construct_checkout_message(i)
        k = k + int(i['c']) * float(i['price'])
    return out + construct_final_checkout_message(k, customer)
