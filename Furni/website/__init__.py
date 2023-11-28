
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import login_user, LoginManager, login_required, logout_user, current_user


app = Flask(__name__)
app.config.from_object('config') 
bcrypt= Bcrypt(app)
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view="login"
migrate = Migrate(app, db, render_as_batch=True)

    
from .views import views
app.register_blueprint(views, url_prefix='/')




