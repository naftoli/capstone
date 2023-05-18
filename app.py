from flask import Flask
from flask_cors import CORS
from api import api
from models import setup_db, db

# create and configure the app
def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app)
    app.secret_key = 'naftoli'
    with app.app_context():
        db.create_all()
    return app

app = create_app()
app.register_blueprint(api)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)