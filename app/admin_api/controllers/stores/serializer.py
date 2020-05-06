from marshmallow import fields
from app.data.models import Store
from core.extensions import ma


class StoreSerializer(ma.ModelSchema):
    class Meta:
        model = Store
