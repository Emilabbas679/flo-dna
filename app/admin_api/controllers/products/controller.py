from flask import request
from connexion import problem
from sqlalchemy import desc

from app.data.models import Product, ProductTag, ProductAttributeValue, ProductAttribute, ProductCourier, \
    ProductCountry, ProductDetail
from app.utils.data_utils import get_paginated_results
from app.utils.helpers import generate_sku
from .serializer import ProductSerializer

serializer = ProductSerializer()


def search(limit=100, page=1, sort=None, q=None):
    search_query = None
    return get_paginated_results(request, Product, serializer, limit, page, search_query)


def get(product_id):
    product = Product.get(id=product_id)
    return serializer.dump(product) or problem(status=404, title='Do not exists',
                                               detail='Product with given ID do not exists')


def post(body):
    courier = None
    attribute_values = None
    details = None
    product_data = body
    product_data.pop('image')
    tags = product_data.pop('tags')
    if 'attribute_values' in product_data.keys():
        attribute_values = product_data.pop('attribute_values')
    if 'courier' in product_data.keys():
        courier = product_data.pop('courier')
    if 'details' in product_data.keys():
        details = product_data.pop('details')
    product_data['sku'] = generate_sku()
    product = Product.create(**product_data)
    for tag in tags:
        ProductTag.create(product_id=product.id, tag_id=tag)
    if attribute_values is not None:
        for value in attribute_values:
            product_attribute = ProductAttribute.create(product_id=product.id,
                                                        attribute_id=value['attribute_id'])
            for v in value['values']:
                ProductAttributeValue.create(product_id=product.id,
                                             product_attribute_id=product_attribute.id,
                                             attribute_id=value['attribute_id'],
                                             attribute_value_id=v)
    if details is not None:
        for det in details:
            ProductDetail.create(product_id=product.id,
                                 country_id=det['country_id'],
                                 price=det['price'],
                                 quantity=det['quantity'],
                                 discount_price=det['discount_price'],
                                 status=det['status'],
                                 name=det['name'],
                                 description=det['description']
                                 )
    if courier is not None:
        for c in courier:
            ProductCourier.create(
                product_id=product.id,
                **c
            )

    return {'id': product.id}


def put(product_id, body):
    courier = None
    attribute_values = None
    details = None
    product_data = body
    tags = product_data.pop('tags')
    product_data.pop('image')
    if product_data['product_type_id'] is None:
        product_data.pop('product_type_id')
    if 'attribute_values' in product_data.keys():
        attribute_values = product_data.pop('attribute_values')
    if 'courier' in product_data.keys():
        courier = product_data.pop('courier')
    if 'details' in product_data.keys():
        details = product_data.pop('details')
    existing_product = Product.get(id=product_id)
    if existing_product:
        existing_product.update(**product_data)
        if tags is not None:
            old_tags = ProductTag.all(product_id=existing_product.id)
            for t in old_tags:
                t.delete()
            for tag in tags:
                t = ProductTag.create(product_id=existing_product.id, tag_id=tag)
        if attribute_values is not None:
            old_attributes = ProductAttribute.all(product_id=existing_product.id)
            for a in old_attributes:
                a.delete()
            old_values = ProductAttributeValue.all(product_id=existing_product.id)
            for v in old_values:
                v.delete()
            for value in attribute_values:
                product_attribute = ProductAttribute.create(product_id=existing_product.id,
                                                            attribute_id=value['attribute_id'])
                for v in value['values']:
                    ProductAttributeValue.create(product_id=existing_product.id,
                                                 product_attribute_id=product_attribute.id,
                                                 attribute_id=value['attribute_id'],
                                                 attribute_value_id=v)
        if details is not None:
            old_details = ProductDetail.all(product_id=existing_product.id)
            for d in old_details:
                d.delete()
            for det in details:
                ProductDetail.create(product_id=existing_product.id,
                                     country_id=det['country_id'],
                                     price=det['price'],
                                     quantity=det['quantity'],
                                     discount_price=det['discount_price'],
                                     status=det['status'],
                                     name=det['name'],
                                     description=det['description']
                                     )
        if courier is not None:
            old_courier = ProductCourier.all(product_id=existing_product.id)
            for cr in old_courier:
                cr.delete()
            for c in courier:
                if 'product_id' in c.keys():
                    c.pop('product_id')
                ProductCourier.create(
                    product_id=existing_product.id,
                    **c
                )
    else:
        return problem(status=404, title='Do not exists',
                       detail='Product with given ID do not exists')
    return serializer.dump(existing_product)
