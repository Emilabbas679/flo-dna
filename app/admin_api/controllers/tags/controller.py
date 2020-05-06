import json

from flask import request
from connexion import problem
from sqlalchemy import desc

from app.data.models import Tag
from app.utils.data_utils import get_paginated_results
from .serializer import TagSerializer

serializer = TagSerializer()


def search(limit=100, page=1, sort=None, q=None):
    search_query = None
    response = get_paginated_results(request, Tag, serializer, limit, page, search_query)
    return response


def get(tag_id):
    country = Tag.get(id=tag_id)
    return serializer.dump(country) or problem(status=404, title='Do not exists',
                                              detail='Tag with given ID do not exists')


def post(body):
    tag_data = body
    country = Tag.create(**tag_data)

    return {'id': country.id}


def put(tag_id, body):
    existing_tag = Tag.get(id=tag_id)
    if existing_tag:
        tag_data = body
        existing_tag.update(**body)

    else:
        return problem(status=404, title='Do not exists',
                       detail='Tag with given ID do not exists')
    return serializer.dump(existing_tag)

