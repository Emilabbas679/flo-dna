import json

from flask import request
from connexion import problem
from sqlalchemy import desc

from app.data.models import Attribute, AttributeValue
from app.utils.data_utils import get_paginated_results
from .serializer import AttributeSerializer

serializer = AttributeSerializer()


def search(limit=100, page=1, sort=None, q=None):
    search_query = None
    response = get_paginated_results(request, Attribute, serializer, limit, page, search_query)
    return response


def get(attribute_id):
    attribute = Attribute.get(id=attribute_id)
    return serializer.dump(attribute) or problem(status=404, title='Do not exists',
                                                    detail='Attribute with given ID do not exists')


def post(body):
    attribute_data = body
    if 'values' in attribute_data.keys():
        values = attribute_data.pop('values')
        attribute = Attribute.create(**attribute_data)
        for value in values:
            AttributeValue.create(attribute_id=attribute.id, **value)
    else:
        attribute = Attribute.create(**attribute_data)
    return {'id': attribute.id}


def put(attribute_id, body):
    attribute_data = body
    existing_attribute = Attribute.get(id=attribute_id)
    if existing_attribute:
        if 'values' in attribute_data.keys():
            values = attribute_data.pop('values')
            existing_attribute.update(**attribute_data)
            for value in values:
                if 'id' in value.keys():
                    existing_value = AttributeValue.get(id=value['id'])
                    if existing_value:
                        existing_value.update(**value)
                else:
                    existing_value = AttributeValue.create(attribute_id=existing_attribute.id, **value)
        else:
            existing_attribute.update(**attribute_data)
    else:
        return problem(status=404, title='Do not exists',
                       detail='Attribute with given ID do not exists')
    return serializer.dump(existing_attribute)


def delete(attribute_id):
    attribute = Attribute.get(id=attribute_id)
    deleted_attribute = attribute
    attribute.delete()
    return serializer.dump(deleted_attribute), 200
