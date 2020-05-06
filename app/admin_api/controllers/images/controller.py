from connexion import NoContent
from flask import current_app, request

from app.data.models import Media
from .serializer import ImageSerializer


logger = current_app.logger
serializer = ImageSerializer()


def put(image_id, body):
    img = Media.create(id=image_id, **body)
    status = 201

    return {'id': img.id}, status


def get(image_id):
    page = Media.get(id=image_id)
    return serializer.dump(page).data or (NoContent, 404)


def search(limit=100, page_number=1):
    images = Media.query.paginate(page_number, limit, False)
    images_page = {
        'items': serializer.dump(images.items, many=True).data or []
    }

    if images.has_next:
        next_num = images.next_num
        images_page['next'] = {
            'next_page_number': next_num,
            'href': f'{request.base_url}?limit={limit}&page_number={next_num}'
        }

    return images_page
