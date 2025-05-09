from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey, Column, Table, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

db = SQLAlchemy()

class Users(db.Model):
    __tablename__='users'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean())
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(120), nullable=False)

    # relationship with other tables
    followers: Mapped[list["Followers"]] = relationship(back_populates="user_from")
    following: Mapped[list["Followers"]] = relationship(back_populates="user_to")
    posts: Mapped[list["Posts"]] = relationship(back_populates="user")
    comments: Mapped["Comments"] = relationship(back_populates="user")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "first name": self.first_name,
            "last name": self.last_name,
            "posts": [post.serialize() for post in self.posts],
            "followers": [follower.serialize() for follower in self.followers],
            "following": [follow.serialize() for follow in self.following]
            # do not serialize the password, its a security breach
        }
    
class Followers(db.Model):
    __tablename__='followers'
    user_from_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    user_to_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)

    # relationship with other tables
    user_from: Mapped["Users"] = relationship(back_populates="followers")
    user_to: Mapped["Users"] = relationship(back_populates="following")

    def serialize(self):
        return {
            "followers": self.user_from_id,
            "following": self.user_to_id
        }

class Posts(db.Model):
    __tablename__='posts'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    # relationship with other tables
    user: Mapped["Users"] = relationship(back_populates="posts")
    comments: Mapped[list["Comments"]] = relationship(back_populates="posts")
    media: Mapped["Media"] = relationship(back_populates="posts")

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user_id,
            "comments": [comment.serialize() for comment in self.comments],
            "media": [type.serialize() for type in self.media]
        }

class Comments(db.Model):
    __tablename__='comments'
    id: Mapped[int] = mapped_column(primary_key=True)
    comment_text: Mapped[str] = mapped_column(String(250))
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"), nullable=False)

    # relationship with other tables
    posts: Mapped["Posts"] = relationship(back_populates="comments")
    user: Mapped["Users"] = relationship(back_populates="comments")

    def serialize(self):
        return {
            "id": self.id,
            "comment": self.comment_text,
            "author": self.author_id,
            "post": self.post_id
        }
    
class MediaType(enum.Enum):
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"
    
class Media(db.Model):
    __tablename__='media'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    type_media: Mapped[MediaType] = mapped_column(nullable=False)
    url: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"), nullable=False)

    # relationship with other tables
    posts: Mapped["Posts"] = relationship(back_populates="media")

    def serialize(self):
        return {
            "id": self.id,
            "type": self.type_media.value,
            "link": self.url,
            "post": self.post.serialize() if self.post else None
        }