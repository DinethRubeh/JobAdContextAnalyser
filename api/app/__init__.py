from flask import Flask
from flask_cors import CORS

# import blueprint objects
from .search.routes import search
from .scrape.routes import scrape

# function to create a flask app using blueprints
def create_app():
    # Initialize flask app
    app = Flask(__name__)
    
    # Handling CORS in Flask
    CORS(app, supports_credentials=True)

    # Resource specific CORS
    # CORS(app,  resources={r"/*": {"origins": "*"}}, supports_credentials=True, expose_headers='Authorization')

    # For browsers to allow POST requests with a JSON content type, the Content-Type header must be allowed.
    app.config['CORS_HEADERS'] = 'Content-Type'

    # register flask blueprints
    with app.app_context():
        app.register_blueprint(search, url_prefix="/topjobs")
        app.register_blueprint(scrape, url_prefix="/topjobs")

    return app