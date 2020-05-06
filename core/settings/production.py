from core.settings.base import Config


class ProductionConfig(Config):
    """ Configuration class for site production environment """

    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = "postgresql://flocake:mua7ren9cpv753rs@flocake-prod-new-do-user-6879125-0.a.db.ondigitalocean.com:25060/flocake_prod?sslmode=require"
