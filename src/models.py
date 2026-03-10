from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'user'  // ✅ Definición correcta de la tabla
    id: Mapped[int] = mapped_column(primary_key=True)  // ✅ Campo ID como clave primaria
    user_name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)  // 📝 Cambié 'username' a 'user_name' para evitar confusión
    first_name: Mapped[str] = mapped_column(String(120), nullable=False)  // 📝 Cambié 'firstname' a 'first_name' para mantener consistencia
    last_name: Mapped[str] = mapped_column(String(120), nullable=False)  // 📝 Cambié 'lastname' a 'last_name' para mantener consistencia
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)  // ✅ Campo de email único
    password: Mapped[str] = mapped_column(String(80), nullable=False)  // 📝 Considera aumentar la longitud de la contraseña para mayor seguridad
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)  // ✅ Campo para indicar si el usuario está activo
    # Relaciones basicas
    posts: Mapped[List["Post"]] = relationship(back_populates="author")  // ✅ Relación con posts
    comments: Mapped[List["Comment"]] = relationship(back_populates="author")  // ✅ Relación con comentarios
    #  Relaciones de seguimiento
    followers: Mapped[List["Follower"]] = relationship(back_populates="user_to", foreign_keys="Follower.user_to_id")  // 📝 Asegúrate de que 'user_to' esté definido correctamente en Follower
    following: Mapped[List["Follower"]] = relationship(back_populates="user_from", foreign_keys="Follower.user_from_id")  // 📝 Asegúrate de que 'user_from' esté definido correctamente en Follower

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.user_name,
            "firstname": self.first_name,
            "lastname": self.last_name,
        }


class Post(db.Model):
    __tablename__ = 'post'  // ✅ Definición correcta de la tabla
    id: Mapped[int] = mapped_column(primary_key=True)  // ✅ Campo ID como clave primaria
    # Relaciones basicas
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)  // ✅ Relación con el usuario
    author: Mapped["User"] = relationship(back_populates="posts")  // ✅ Relación con el autor
    media: Mapped[List["Media"]] = relationship(back_populates="post")  // ✅ Relación con media
    comments: Mapped[List["Comment"]] = relationship(back_populates="post")  // ✅ Relación con comentarios

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id
        }


class Media(db.Model):
    __tablename__ = 'media'  // ✅ Definición correcta de la tabla
    id: Mapped[int] = mapped_column(primary_key=True)  // ✅ Campo ID como clave primaria
    type: Mapped[str] = mapped_column(String(50), nullable=False)  // ✅ Campo para tipo de media
    url: Mapped[str] = mapped_column(String(120), nullable=False)  // ✅ Campo para URL de media
    # Relaciones basicas
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"), nullable=False)  // ✅ Relación con post
    post: Mapped["Post"] = relationship(back_populates="media")  // ✅ Relación con post

    def serialize(self):
        return {
            "id": self.id,
            "type": self.type,
            "url": self.url,
        }

class Comment(db.Model):
    __tablename__ = 'comment'  // ✅ Definición correcta de la tabla
    id: Mapped[int] = mapped_column(primary_key=True)  // ✅ Campo ID como clave primaria
    comment_text: Mapped[str] = mapped_column(String(500), nullable=False)  // ✅ Campo para texto del comentario
    # Relaciones basicas
    author_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)  // ✅ Relación con el autor
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"), nullable=False)  // ✅ Relación con el post
    author: Mapped["User"] = relationship(back_populates="comments")  // ✅ Relación con el autor
    post: Mapped["Post"] = relationship(back_populates="comments")  // ✅ Relación con el post

    def serialize(self):
        return {
                "id": self.id,
                "comment_text": self.comment_text
        }

class Follower(db.Model):
    __tablename__ = 'follower'  // ✅ Definición correcta de la tabla
    id: Mapped[int] = mapped_column(primary_key=True)  // ✅ Campo ID como clave primaria
    # Relaciones de seguimiento
    user_from_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)  // ✅ Relación con el usuario que sigue
    user_to_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)  // ✅ Relación con el usuario seguido
    user_from: Mapped["User"] = relationship(back_populates="following", foreign_keys=[user_from_id])  // ✅ Relación con el usuario que sigue
    user_to: Mapped["User"] = relationship(back_populates="followers", foreign_keys=[user_to_id])  // ✅ Relación con el usuario seguido

    def serialize(self):
        return {
            "id": self.id,
            "user_from_id": self.user_from_id,
            "user_to_id": self.user_to_id,
        }