import random
from io import BytesIO

import connexion
import requests
from connexion import NoContent
from flask import current_app, request

from app.data.models import Media, LandingPage, Product, ProductMedia, ProductDetail
from app.utils.data_utils import get_paginated_results
from app.utils.helpers import upload_file_to_spaces
from .serializer import ImageSerializer
from boto3 import session
from botocore.client import Config
from PIL import Image

session = session.Session()

logger = current_app.logger
serializer = ImageSerializer()

quality = '70'


def search(limit=100, page=1, product=None, sort=None, q=None):
    search_query = None
    kwargs = {}
    if product is not None:
        kwargs['product_id'] = product
    response = get_paginated_results(request, ProductMedia, serializer, limit, page, search_query, **kwargs)
    return response


def put(image_id, body):
    img = Media.create(id=image_id, **body)
    status = 201

    return {'id': img.id}, status


def delete(file_id):
    img = ProductMedia.get(id=file_id)
    img.delete()
    return {
        "status": True
           }, 200


def post():
    file_to_upload = connexion.request.files['file']
    entity_id = connexion.request.form['entity_id']
    entity_key = connexion.request.form['entity_key']
    file_key = ''

    if entity_key == 'landing-pages':
        entity = LandingPage.get(id=entity_id)
        file_key = entity.title.replace(' ', '-').lower()
    elif entity_key == 'products':
        entity = ProductDetail.get(product_id=entity_id)
        file_key = entity.name['az'].replace(' ', '-').lower()

    ext = file_to_upload.filename.split('.')[-1]
    name = random.randrange(0, 2000000000)
    file_name = (file_key + '-' + str(name) + '.' + ext)
    webp_filename = (file_key + '-' + str(name) + '-webp.' + 'webp')

    if entity_key == 'landing-pages':
        # original_mem_file = BytesIO()
        # file_to_upload.save(original_mem_file)
        # original_mem_file.seek(0)
        upload_url = f'{entity_key}/{file_name}'
        upload_file_to_spaces('flocake-cdn', file_to_upload, upload_url, file_to_upload.content_type, 'public-read')
    elif entity_key == 'products':
        pr_image = Image.open(file_to_upload)
        original_mem_file = BytesIO()
        pr_image.save(original_mem_file, pr_image.format)
        original_mem_file.seek(0)
        upload_url = f'{entity_key}/{entity_id}/{file_name}'
        webp_url = f'{entity_key}/{entity_id}/{webp_filename}'
        webp_image = img_to_webp(file_to_upload)

        upload_file_to_spaces('flocake-cdn', original_mem_file, upload_url, file_to_upload.content_type, 'public-read')
        upload_file_to_spaces('flocake-cdn', webp_image, webp_url, 'image/webp', 'public-read')
        # generate thumbnail with pillow and upload to s3
        pil_image = Image.open(file_to_upload)
        thumbnail = pil_image.resize((400, 400))
        # logo = Image.open(requests.get('https://www.aybax.com/pages/public/res/logo/az/fixlogo1.png', stream=True).raw)
        # position = (int((thumbnail.width - logo.width)/2), int((thumbnail.height - logo.height)/2))
        # thumbnail.paste(logo, position, logo)
        thumbnail_mem_file = BytesIO()
        thumbnail.save(thumbnail_mem_file, pil_image.format)
        thumbnail_mem_file.seek(0)
        thumbnail_upload_url = f'{entity_key}/{entity_id}/thumbnail/{file_name}'
        upload_file_to_spaces('flocake-cdn', thumbnail_mem_file, thumbnail_upload_url, file_to_upload.content_type, 'public-read')
        image_sizes = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
        for s in image_sizes:
            upload_file(file_to_upload, entity_key, entity_id, file_name, file_to_upload.content_type, s, webp_filename)
    if entity_key == 'products':
        media = ProductMedia.create(product_id=entity_id, entity_key=entity_key, title=file_name, file_name=file_name,
                             content_type=file_to_upload.content_type)
    else:
        media = Media.create(entity_id=entity_id, entity_key=entity_key, title=file_name, file_name=file_name,
                             content_type=file_to_upload.content_type)
    return 'ok', 201


def upload_file(file, entity_key, entity_id, file_name, content_type, size, webp_filename):
    pil_image = Image.open(file)
    thumbnail = pil_image.resize((size, size))
    # logo = Image.open(requests.get(f'https://flocake-cdn.fra1.digitaloceanspaces.com/assets/watermark/watermark-{size}_x_{size}.png', stream=True).raw)
    # position = (int((thumbnail.width - logo.width) / 2), int((thumbnail.height - logo.height) / 2))
    # thumbnail.paste(logo, logo)
    thumbnail_mem_file = BytesIO()
    thumbnail.save(thumbnail_mem_file, pil_image.format)
    thumbnail_mem_file.seek(0)
    thumbnail_upload_url = f'{entity_key}/{entity_id}/thumbnail/{size}/{file_name}'
    upload_file_to_spaces('flocake-cdn', thumbnail_mem_file, thumbnail_upload_url, content_type,
                          'public-read')
    webp_url = f'{entity_key}/{entity_id}/thumbnail/{size}/{webp_filename}'
    webp_image = img_to_webp(thumbnail_mem_file)
    upload_file_to_spaces('flocake-cdn', webp_image, webp_url, 'image/webp',
                          'public-read')


def img_to_webp(image):
    img = Image.open(image)
    webp_image = BytesIO()
    img.save(webp_image, 'webp')
    webp_image.seek(0)
    return webp_image
