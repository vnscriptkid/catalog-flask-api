from flask import Flask
from flask_marshmallow import Marshmallow
from flask_restplus import Api

from db import db
from controllers.category import api as category_api
from controllers.article import api as article_api

# Init app
app = Flask(__name__)
api = Api(app, title="Restful API", description="Blogging App")

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['RESTPLUS_VALIDATE'] = True

# Init DB
db.init_app(app)
ma = Marshmallow(app)


@app.before_first_request
def create_tables():
    db.create_all()


# article_ns = api.namespace('articles', description="Article operations")
api.add_namespace(article_api)
api.add_namespace(category_api)

# Run server
if __name__ == '__main__':
    app.run(debug=True)
