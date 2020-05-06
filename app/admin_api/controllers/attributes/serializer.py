from marshmallow import fields, post_dump

from app.admin_api.controllers.attribute_values import AttributeValueSerializer
from core.extensions import ma
from app.data.models import Attribute


class AttributeSerializer(ma.ModelSchema):
    class Meta:
        model = Attribute

    values = fields.Nested(AttributeValueSerializer, many=True)

