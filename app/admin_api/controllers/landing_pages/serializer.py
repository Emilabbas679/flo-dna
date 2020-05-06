from marshmallow import fields, post_dump

from core.extensions import ma
from app.data.models import LandingPage, Media


class ImageSerializer(ma.ModelSchema):
    class Meta:
        model = Media
        fields = ('id', 'file_name', 'content_type', 'title', 'src')


class LandingPageSerializer(ma.ModelSchema):
    class Meta:
        model = LandingPage
        include_fk = True
    image = fields.Nested(ImageSerializer)

