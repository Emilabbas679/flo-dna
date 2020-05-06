from flask import request
from connexion import problem
from sqlalchemy import desc

from app.data.models import LandingPage, Media, LandingTag
from app.utils.helpers import delete_file_from_spaces
from .serializer import LandingPageSerializer

serializer = LandingPageSerializer()


def search(limit=100, page=1, sort=None, q=None):
    landings = LandingPage.query.order_by(desc(LandingPage.updated)).paginate(page, limit)

    response = {
        'data': serializer.dump(landings.items, many=True) or [],
        'total': landings.total
    }

    if landings.has_next:
        next_num = landings.next_num
        response['next'] = {
            'next_page_number': next_num,
            'href':  f'{request.base_url}?limit={limit}&page_number={next_num}'
        }
    return response


def get(landing_id):
    landing = LandingPage.get(id=landing_id)
    return serializer.dump(landing) or problem(status=404, title='Do not exists',
                                              detail='Driver with given ID do not exists')


def post(body):
    landing_data = body
    if 'image' in landing_data.keys():
        landing_data.pop('image')
    if 'tags' in landing_data.keys():
        tags = landing_data.pop('tags')
    landing = LandingPage.create(**landing_data)
    if 'tags' in body.keys() and tags is not None:
        for tag in tags:
            LandingTag.create(landing_id=landing.id, tag_id=tag)

    return {'id': landing.id}


def put(landing_id, body):
    global tags
    landing_data = body
    img = landing_data.pop('image')
    landing_data.pop('language')
    landing_data.pop('country')
    if 'tags' in landing_data.keys():
        tags = landing_data.pop('tags')
    existing_landing = LandingPage.get(id=landing_id)
    if existing_landing:
        if img is None:
            key = f'landing-pages/{existing_landing.image.file_name}'
            delete_file_from_spaces('flocake-cdn', key)
            existing_landing.image.delete()
        else:
            if 'id' in img and img['id'] is None:
                key = f'landing-pages/{existing_landing.image.file_name}'
                delete_file_from_spaces('flocake-cdn', key)
                existing_landing.image.delete()
        if tags is not None:
            old_tags = LandingTag.all(landing_id=existing_landing.id)
            for t in old_tags:
                t.delete()
            for tag in tags:
                t = LandingTag.create(landing_id=existing_landing.id, tag_id=tag)
        existing_landing.update(**landing_data)
    else:
        return problem(status=404, title='Do not exists',
                       detail='Driver with given ID do not exists')
    return serializer.dump(existing_landing)

