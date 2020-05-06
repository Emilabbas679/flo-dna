import json

from flask import request
from connexion import problem
from sqlalchemy import desc

from app.data.models import HelpArticle
from app.utils.data_utils import get_paginated_results
from .serializer import HelpArticleSerializer

serializer = HelpArticleSerializer()


def search(limit=100, page=1, sort=None, q=None):
    search_query = None
    response = get_paginated_results(request, HelpArticle, serializer, limit, page, search_query)
    return response


def get(help_article_id):
    category = HelpArticle.get(id=help_article_id)
    return serializer.dump(category) or problem(status=404, title='Do not exists',
                                                detail='Tag with given ID do not exists')


def post(body):
    tag_data = body
    country = HelpArticle.create(**tag_data)

    return {'id': country.id}


def put(help_article_id, body):
    existing_tag = HelpArticle.get(id=help_article_id)
    if existing_tag:
        tag_data = body
        if 'category' in tag_data.keys():
            tag_data.pop('category')
        existing_tag.update(**tag_data)

    else:
        return problem(status=404, title='Do not exists',
                       detail='Tag with given ID do not exists')
    return serializer.dump(existing_tag)
