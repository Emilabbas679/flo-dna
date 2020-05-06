from marshmallow import fields, post_dump

from core.extensions import ma
from app.data.models import Language


class LanguageSerializer(ma.ModelSchema):
    class Meta:
        model = Language
        fields = ('id', 'created', 'updated', 'name', 'code', 'status')
