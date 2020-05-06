from core.extensions import ma
from app.data.models import Media, ProductMedia


class ImageSerializer(ma.ModelSchema):
    class Meta:
        model = ProductMedia
        fields = ('id', 'file_name', 'content_type', 'title', 'src')
