from app.data.models import Customer
from app.utils.data_utils import get_paginated_results
from .serializer import CustomerSerializer
from flask import request
from connexion import NoContent

serializer = CustomerSerializer()


def search(limit=20, page=1, sort=None, q=None):
    search_query = None
    return get_paginated_results(request, Customer, serializer, limit, page, search_query)


def get(customer_id):
    customer = Customer.get(id=customer_id)
    response = {
        'data': serializer.dump(customer)
    }
    return response, 200


def put(customer_id, body):
    customer_data = body
    customer = Customer.get(id=customer_id)
    customer.update(**customer_data)
    response = {
        'data': serializer.dump(customer)
    }

    return response, 200


def post(body):
    customer_data = body
    customer = Customer.create(**customer_data)
    response = {
        'data': serializer.dump(customer)
    }

    return response, 201
