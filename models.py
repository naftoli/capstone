import os
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

database_filename = "database.db"
project_dir = os.path.dirname(os.path.abspath(__file__))
database_path = "sqlite:///{}".format(os.path.join(project_dir, database_filename))

def setup_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)

''' create a user model that includes first name, last name, email, and password '''
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String())
    last_name = db.Column(db.String())
    email = db.Column(db.String())
    password = db.Column(db.String())

    def __init__(self, first_name, last_name, email, password):
        self.first_name=first_name
        self.last_name=last_name
        self.email=email
        self.password=password

    def __repr__(self):
        return f'<User {self.id} {self.first_name} {self.last_name} {self.email} {self.password}>'

    def get_favorite_links(self):
        return Favorite.query.filter(Favorite.user_id == self.id).all()

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email
        }

''' create a model for storing user favorite links '''
class Favorite(db.Model):
    __tablename__ = 'favorites'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    link = db.Column(db.String())

    def __init__(self, user_id, link):
        self.user_id=user_id
        self.link=link

    def __repr__(self):
        return f'<Favorite {self.id} {self.user_id} {self.link}>'

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'link': self.link
        }

