from flask import current_app
from connexion import ProblemException

import app.utils.helpers as utils
from app.data.models import Media


logger = current_app.logger


def search(image_id):
    img = Media.get(id=image_id)
    if not img:
        raise ProblemException(title='Does not exists',
                               detail='Image with given id does not exists')

    response = utils.create_presigned_post('flocake-cdn', img.file_name)
    return response
