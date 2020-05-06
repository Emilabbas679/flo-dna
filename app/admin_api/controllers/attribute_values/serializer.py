from marshmallow import fields, post_dump

from core.extensions import ma
from app.data.models import AttributeValue


class AttributeValueSerializer(ma.ModelSchema):
    class Meta:
        model = AttributeValue
        include_fk = True
