from marshmallow import fields
from app.data.models import Customer
from core.extensions import ma


class CustomerSerializer(ma.ModelSchema):
    class Meta:
        model = Customer
        include_fk = True
