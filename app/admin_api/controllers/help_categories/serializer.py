from marshmallow import fields
from app.data.models import HelpCategory
from core.extensions import ma


class HelpCategorySerializer(ma.ModelSchema):
    class Meta:
        model = HelpCategory
        include_fk = True
