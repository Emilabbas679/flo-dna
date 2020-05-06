from marshmallow import fields, post_dump

from core.extensions import ma
from app.data.models import Country


class CountrySerializer(ma.ModelSchema):
    class Meta:
        model = Country
        fields = ('id', 'created', 'updated', 'name', 'code', 'status')
