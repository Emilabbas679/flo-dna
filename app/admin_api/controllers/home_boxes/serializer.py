from marshmallow import fields, post_dump

from core.extensions import ma
from app.data.models import HomeBox


class HomeBoxSerializer(ma.ModelSchema):
    class Meta:
        model = HomeBox
        include_fk = True
