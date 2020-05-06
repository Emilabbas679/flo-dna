from marshmallow import fields
from app.data.models import HelpArticle
from core.extensions import ma


class HelpArticleSerializer(ma.ModelSchema):
    class Meta:
        model = HelpArticle
        include_fk = True
