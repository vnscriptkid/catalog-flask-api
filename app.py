from flask import Flask
from flask_restplus import Api
from flask_jwt import JWT

from debug import sql_debug
from security import authenticate, identity
from db import db
from controllers.category import api as category_api
from controllers.article import api as article_api
from controllers.user import api as user_api
# from controllers.user import UserRegister

# Init app
app = Flask(__name__)
api = Api(app, title="Restful API", description="Blogging App")

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['RESTPLUS_VALIDATE'] = True
app.secret_key = 'keep it in ur pocket!'


app.after_request(sql_debug)

# Init DB
db.init_app(app)


@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWT(app, authenticate, identity)
api.add_namespace(article_api)
api.add_namespace(category_api)
api.add_namespace(user_api)

# Run server
if __name__ == '__main__':
    app.run(debug=True)
