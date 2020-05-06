from core.extensions import ma
from app.data.models import Media


class ImageSerializer(ma.ModelSchema):
    class Meta:
        model = Media
