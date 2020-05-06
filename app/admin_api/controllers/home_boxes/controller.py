import json

from flask import request
from connexion import problem
from sqlalchemy import desc

from app.data.models import HomeBox, HomeBoxTag, HomeBoxLanding
from app.utils.data_utils import get_paginated_results
from .serializer import HomeBoxSerializer

serializer = HomeBoxSerializer()


def search(limit=100, page=1, sort=None, q=None):
    search_query = None
    response = get_paginated_results(request, HomeBox, serializer, limit, page, search_query)
    return response


def get(home_box_id):
    home_box = HomeBox.get(id=home_box_id)
    return serializer.dump(home_box) or problem(status=404, title='Do not exists',
                                              detail='Tag with given ID do not exists')


def post(body):
    home_box_data = body
    tags = None
    landings = None
    if 'tags' in home_box_data.keys():
        tags = home_box_data.pop('tags')
    if 'landings' in home_box_data.keys():
        landings = home_box_data.pop('landings')
    home_box = HomeBox.create(**home_box_data)

    if tags is not None:
        for tag in tags:
            HomeBoxTag.create(box_id=home_box.id, tag_id=tag)
    if landings is not None:
        for landing in landings:
            HomeBoxLanding.create(box_id=home_box.id, landing_id=landing)

    return {'id': home_box.id}


def put(home_box_id, body):
    existing_home_box = HomeBox.get(id=home_box_id)
    tags = None
    landings = None
    if existing_home_box:
        home_box_data = body
        if 'tags' in home_box_data.keys():
            tags = home_box_data.pop('tags')
        if 'landings' in home_box_data.keys():
            landings = home_box_data.pop('landings')
        existing_home_box.update(**body)
        if tags is not None:
            old_tags = HomeBoxTag.all(box_id=existing_home_box.id)
            for t in old_tags:
                t.delete()
            for tag in tags:
                t = HomeBoxTag.create(box_id=existing_home_box.id, tag_id=tag)
        if landings is not None:
            old_landings = HomeBoxLanding.all(box_id=existing_home_box.id)
            for land in old_landings:
                land.delete()
            for landing in landings:
                HomeBoxLanding.create(box_id=existing_home_box.id, landing_id=landing)

    else:
        return problem(status=404, title='Do not exists',
                       detail='Tag with given ID do not exists')
    return serializer.dump(existing_home_box)

