from app.data.models import Store
from app.utils.data_utils import get_paginated_results
from .serializer import StoreSerializer
from flask import request
from connexion import NoContent
serializer = StoreSerializer(exclude=['password'])


def search(limit=20, page=1, sort=None, q=None):
    search_query = None
    return get_paginated_results(request, Store, serializer, limit, page, search_query)


def get(store_id):
    store = Store.get(id=store_id)
    response = {
        'data': serializer.dump(store)
    }
    return response, 200


def put(store_id, body):
    store = Store.get(id=store_id)
    store_data = body
    store.update(**store_data)
    response = {
        'data': serializer.dump(store)
    }

    return response, 200


def post(body):
    store_data = body
    store = Store.create(**store_data)
    response = {
        'data': serializer.dump(store)
    }

    return response, 201
