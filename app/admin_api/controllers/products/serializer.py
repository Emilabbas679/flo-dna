from marshmallow import fields, post_dump

from app.admin_api.controllers.attribute_values import AttributeValueSerializer
from app.admin_api.controllers.landing_pages.serializer import ImageSerializer
from app.admin_api.controllers.tags import TagSerializer
from core.extensions import ma
from app.data.models import Product, ProductAttribute, ProductMedia, ProductCourier, ProductDetail


class ProductAttributeSerializer(ma.ModelSchema):
    class Meta:
        model = ProductAttribute
        include_fk = True


class ProductCourierSerializer(ma.ModelSchema):
    class Meta:
        model = ProductCourier
        include_fk = True


class ProductImageSerializer(ma.ModelSchema):
    class Meta:
        model = ProductMedia
        fields = ('id', 'file_name', 'content_type', 'title', 'src')


class ProductDetailSerializer(ma.ModelSchema):
    class Meta:
        model = ProductDetail
        include_fk = True


class ProductSerializer(ma.ModelSchema):
    class Meta:
        model = Product
        include_fk = True

    image = fields.Nested(ProductImageSerializer, many=True)
    attribute_values = fields.Nested(ProductAttributeSerializer, many=True)
    courier = fields.Nested(ProductCourierSerializer, many=True)
    details = fields.Nested(ProductDetailSerializer, many=True)
