from flask import request
from connexion import problem
from sqlalchemy import desc

from app.data.models import ProductType
from .serializer import ProductTypeSerializer

serializer = ProductTypeSerializer()


def search(limit=100, page=1, sort=None, q=None):
    product_types = ProductType.query.order_by(desc(ProductType.updated)).paginate(page, limit)

    response = {
        'data': serializer.dump(product_types.items, many=True) or [],
        'total': product_types.total
    }

    if product_types.has_next:
        next_num = product_types.next_num
        response['next'] = {
            'next_page_number': next_num,
            'href':  f'{request.base_url}?limit={limit}&page_number={next_num}'
        }
    return response


def get(product_type_id):
    product_type = ProductType.get(id=product_type_id)
    return serializer.dump(product_type) or problem(status=404, title='Do not exists',
                                                    detail='ProductType with given ID do not exists')


def post(body):
    product_type_data = body
    product_type = ProductType.create(**product_type_data)

    return {'id': product_type.id}


def put(product_type_id, body):
    product_type_data = body
    existing_product_type = ProductType.get(id=product_type_id)
    if existing_product_type:
        existing_product_type.update(**body)
    else:
        return problem(status=404, title='Do not exists',
                       detail='ProductType with given ID do not exists')
    return serializer.dump(existing_product_type)

