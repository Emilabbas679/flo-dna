from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
# from flask_socketio import SocketIO
from flask_login import LoginManager
from flask_babelex import Babel
from flask_cors import CORS


db = SQLAlchemy()
ma = Marshmallow()
migrator = Migrate(db=db)
jwt = JWTManager()
# socket = SocketIO()
login_manager = LoginManager()
babel = Babel()
cors = CORS()
