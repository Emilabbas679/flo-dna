from flask import request
from connexion import problem
from sqlalchemy import desc

from app.data.models import Category, CategoryTag
from app.utils.data_utils import get_paginated_results
from .serializer import CategorySerializer

serializer = CategorySerializer()


def search(limit=100, page=1, sort=None, q=None):
    search_query = None
    return get_paginated_results(request, Category, serializer, limit, page, search_query)


def get(category_id):
    country = Category.get(id=category_id)
    return serializer.dump(country) or problem(status=404, title='Do not exists',
                                              detail='Category with given ID do not exists')


def post(body):
    global tags
    category_data = body
    if 'tags' in category_data.keys():
        tags = category_data.pop('tags')
    category = Category.create(**category_data)
    if tags is not None:
        for tag in tags:
            CategoryTag.create(category_id=category.id, tag_id=tag)

    return {'id': category.id}


def put(category_id, body):
    existing_category = Category.get(id=category_id)
    if existing_category:
        category_data = body
        tags = category_data.pop('tags')
        existing_category.update(**category_data)
        if tags is not None:
            old_tags = CategoryTag.all(category_id=existing_category.id)
            for t in old_tags:
                t.delete()
            for tag in tags:
                CategoryTag.create(category_id=existing_category.id, tag_id=tag)

    else:
        return problem(status=404, title='Do not exists',
                       detail='Category with given ID do not exists')
    return serializer.dump(existing_category)

