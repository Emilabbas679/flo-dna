from app.data.models import Order
from .serializer import OrderSerializer
from flask import request
from connexion import NoContent
serializer = OrderSerializer()


def search(limit=100, page=1):
    order_query = Order.query
    orders = order_query.paginate(page, limit, False)
    total = order_query.count()
    order = {
        'data': serializer.dump(orders.items, many=True) or [],
        'total': total
    }
    if orders.has_next:
        next_num = order.next_num
        order['next'] = {
            'next_page_number': next_num,
            'href': f'{request.base_url}?limit={limit}&page={next_num}'
        }

    return order, 200


def get(order_id):
    order = Order.get(id=order_id)
    response = {
        'data': serializer.dump(order)
    }
    return response, 200


def put(order_id, **order_input):
    order = Order.get(id=order_id)
    order.update(**order_input['body'])
    response = {
        'data': serializer.dump(order)
    }

    return response, 200


def post(**order_input):
    order = Order.create(**order_input['body'])
    response = {
        'data': serializer.dump(order)
    }

    return response, 201
