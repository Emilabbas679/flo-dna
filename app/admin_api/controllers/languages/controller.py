from flask import request
from connexion import problem
from sqlalchemy import desc

from app.data.models import Language
from .serializer import LanguageSerializer

serializer = LanguageSerializer()


def search(limit=100, page=1, sort=None, q=None):
    languages = Language.query.order_by(desc(Language.updated)).paginate(page, limit)

    response = {
        'data': serializer.dump(languages.items, many=True) or [],
        'total': languages.total
    }

    if languages.has_next:
        next_num = languages.next_num
        response['next'] = {
            'next_page_number': next_num,
            'href':  f'{request.base_url}?limit={limit}&page_number={next_num}'
        }
    return response


def get(language_id):
    language = Language.get(id=language_id)
    return serializer.dump(language) or problem(status=404, title='Do not exists',
                                              detail='Driver with given ID do not exists')


def post(body):
    country_data = body
    language = Language.create(**country_data)

    return {'id': language.id}


def put(language_id, body):
    language_data = body
    existing_language = Language.get(id=language_id)
    if not existing_language:
        return problem(status=404, title='Do not exists',
                       detail='Driver with given ID do not exists')
    else:
        existing_language.update(**body)

    return serializer.dump(existing_language)

