from flask import request
from connexion import problem
from sqlalchemy import desc

from app.data.models import Country
from .serializer import CountrySerializer

serializer = CountrySerializer()


def search(limit=100, page=1, sort=None, q=None):
    countries = Country.query.order_by(desc(Country.updated)).paginate(page, limit)

    response = {
        'data': serializer.dump(countries.items, many=True) or [],
        'total': countries.total
    }

    if countries.has_next:
        next_num = countries.next_num
        response['next'] = {
            'next_page_number': next_num,
            'href':  f'{request.base_url}?limit={limit}&page_number={next_num}'
        }
    return response


def get(country_id):
    country = Country.get(id=country_id)
    return serializer.dump(country) or problem(status=404, title='Do not exists',
                                              detail='Driver with given ID do not exists')


def post(body):
    country_data = body
    country = Country.create(**country_data)

    return {'id': country.id}


def put(country_id, body):
    existing_country = Country.get(id=country_id)
    if existing_country:
        country_data = body
        body.pop('created')
        body.pop('updated')
        existing_country.update(**body)

    else:
        return problem(status=404, title='Do not exists',
                       detail='Driver with given ID do not exists')
    return serializer.dump(existing_country)

