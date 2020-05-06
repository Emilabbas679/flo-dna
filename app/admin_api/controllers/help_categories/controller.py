import json

from flask import request
from connexion import problem
from sqlalchemy import desc

from app.data.models import HelpCategory
from app.utils.data_utils import get_paginated_results
from .serializer import HelpCategorySerializer

serializer = HelpCategorySerializer()


def search(limit=100, page=1, sort=None, q=None):
    search_query = None
    response = get_paginated_results(request, HelpCategory, serializer, limit, page, search_query)
    return response


def get(help_category_id):
    category = HelpCategory.get(id=help_category_id)
    return serializer.dump(category) or problem(status=404, title='Do not exists',
                                              detail='Tag with given ID do not exists')


def post(body):
    tag_data = body
    country = HelpCategory.create(**tag_data)

    return {'id': country.id}


def put(help_category_id, body):
    existing_tag = HelpCategory.get(id=help_category_id)
    if existing_tag:
        tag_data = body
        if 'articles' in tag_data.keys():
            tag_data.pop('articles')
        existing_tag.update(**body)

    else:
        return problem(status=404, title='Do not exists',
                       detail='Tag with given ID do not exists')
    return serializer.dump(existing_tag)

