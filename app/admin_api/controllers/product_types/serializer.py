from marshmallow import fields, post_dump

from core.extensions import ma
from app.data.models import ProductType


class ProductTypeSerializer(ma.ModelSchema):
    class Meta:
        model = ProductType
