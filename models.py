from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, aliased
from sqlalchemy.sql.expression import func

from database import Base

class User(Base):
    __tablename__ = 'User'
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    password = Column(String(120), nullable=False)
    login_id = Column(String(36), nullable=True)
    first_name = Column(String(120), unique=False, nullable=True)
    last_name = Column(String(120), unique=False, nullable=True)
    age = Column(Integer(), unique=False, nullable=True)
    bio = Column(String(512), unique=False, nullable=True)
    profile_pic = Column(String(120), unique=False, nullable=True)


    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    @staticmethod
    def find_another_random(user):
        liked_user_ids = [like.liked_user for like in user.likes]
        return User.query.filter(User.id != user.id,
                User.id.notin_(liked_user_ids)).order_by(func.random()).first()

    def get_id(self):
        return self.login_id

    def __repr__(self):
        return '<User %r>' % self.username

class Topic(Base):
    __tablename__ = "Topic"
    id = Column(Integer, primary_key=True)
    name = Column(String(120))
    description = Column(String(400))


class Post(Base):
    __tablename__ = "Post"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("User.id"))
    topic_id = Column(Integer, ForeignKey("Topic.id"))
    title = Column(String(80), nullable=False)
    content = Column(String(512), nullable=False)