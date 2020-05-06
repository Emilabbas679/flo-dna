from marshmallow import fields
from app.data.models import Order
from core.extensions import ma


class OrderSerializer(ma.ModelSchema):
    class Meta:
        model = Order
        ordered = True