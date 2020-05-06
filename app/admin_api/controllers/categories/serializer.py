from marshmallow import fields, post_dump

from core.extensions import ma
from app.data.models import Category


class CategorySerializer(ma.ModelSchema):
    class Meta:
        model = Category
        include_fk = True

    @post_dump
    def remove_none_values(self, data, many):
        return {
            key: value for key, value in data.items()
            if value is not None
        }
