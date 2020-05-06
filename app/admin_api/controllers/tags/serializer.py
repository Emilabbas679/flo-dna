from marshmallow import fields, post_dump

from core.extensions import ma
from app.data.models import Tag


class TagSerializer(ma.ModelSchema):
    class Meta:
        model = Tag
        include_fk = True
