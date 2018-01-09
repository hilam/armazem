from datetime import datetime
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import enum


# TODO Look for better way of manipulate accepted mime types
class ItemType(enum.Enum):
    url = 1
    image = 2
    pdf = 3
    video = 4
    text = 5


@login.user_loader
def load_user(userid):
    return User.query.get(int(userid))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    items = db.relationship('Item', backref='owner', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Category(db.Model):
    """
    Category class
    """
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Unicode(140), nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    items = db.relationship('Item', backref='category', lazy='dynamic')

    def __str__(self):
        return self.description


item_tags = db.Table('Items_Tags', db.Model.metadata,
                     db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
                     db.Column('item_id', db.Integer, db.ForeignKey('item.id'))
                     )


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Unicode(140), nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    items = db.relationship('Item', backref='tags', lazy='dynamic',
                            secondary=item_tags)

    def __str__(self):
        return self.description


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category = db.Column(db.Integer, db.ForeignKey('category.id'),
                         nullable=False)
    # tags = db.relationship(db.Integer, db.ForeignKey('tag.id'),
    #                       secondary=item_tags)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    description = db.Column(db.Unicode(140), nullable=False)
    item_type = db.Column(db.Enum(ItemType), nullable=False)
    item_file = db.Column(db.BLOB)
    item_content = db.Column(db.BLOB)

    def __str__(self):
        return self.description
