import json

from flask import request
from connexion import problem
from sqlalchemy import desc

from app.data.models import AttributeValue
from app.utils.data_utils import get_paginated_results
from .serializer import AttributeValueSerializer

serializer = AttributeValueSerializer()


def search(attribute_id=None, limit=100, page=1, sort=None, q=None):
    search_query = None
    kwargs = {}
    if attribute_id is not None:
        kwargs['attribute_id'] = attribute_id
    response = get_paginated_results(request, AttributeValue, serializer, limit, page, search_query, **kwargs)
    return response


def get(attribute_value_id):
    attribute_value = AttributeValue.get(id=attribute_value_id)
    return serializer.dump(attribute_value) or problem(status=404, title='Do not exists',
                                                    detail='AttributeValue with given ID do not exists')


def post(body):
    attribute_value_data = body
    attribute_value = AttributeValue.create(**attribute_value_data)

    return {'id': attribute_value.id}


def put(attribute_value_id, body):
    attribute_value_data = body
    existing_attribute_value = AttributeValue.get(id=attribute_value_id)
    if existing_attribute_value:
        existing_attribute_value.update(**body)
    else:
        return problem(status=404, title='Do not exists',
                       detail='AttributeValue with given ID do not exists')
    return serializer.dump(existing_attribute_value)

