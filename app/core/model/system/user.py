# -*- coding: utf-8 -*-
"""User models."""
import jwt
from flask_login import UserMixin
from sqlalchemy import text

from app.core.model.system.blacklist import BlacklistToken
from app.main import config
from app.main.extensions import flask_bcrypt
from app.main.database import (
    Column,
    Model,
    SurrogatePK,
    db,
    reference_col,
    relationship,
)
from app.utils.arrow_time import utc

SECRET_KEY = config.SECRET_KEY


class Role(SurrogatePK, Model):
    """A role for a user."""

    __tablename__ = "roles"
    name = Column(db.String(80), unique=True, nullable=False)
    user_id = reference_col("sys_user", nullable=True)
    user = relationship("User", backref="roles")

    def __init__(self, name, **kwargs):
        """Create instance."""
        db.Model.__init__(self, name=name, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<Role({self.name})>"


class User(UserMixin, SurrogatePK, Model):
    """A user of the app."""

    __tablename__ = "sys_user"
    # id = Column(db.BIGINT(20), primary_key=True, comment='ID')
    user_name = Column(
        db.String(80), nullable=False, server_default=text("''"), comment="用户名"
    )
    email = Column(db.String(80), comment="邮箱")
    # password:The hashed password
    password = Column(db.LargeBinary(128), nullable=False, comment="密码")
    # Phone:Auth uniqueness
    phone = Column(db.String(20), comment="手机号")
    # Admin:Super user
    super_user = Column(db.Boolean(1), server_default=text("'0'"), comment="系统管理员")
    update_by = Column(db.String(80), comment="更新记录")
    create_time = Column(
        db.TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), comment="创建时间"
    )
    # login_time = Column(
    #     db.TIMESTAMP,
    #     server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
    #     comment="登录时间",
    # ) # mysql
    login_time = Column(
        db.TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), comment="登录时间"
    )
    remark = Column(db.String(100), comment="备注")
    state = Column(db.Boolean(1), server_default=text("'1'"), comment="状态(0：禁用，1：启用)")

    def __init__(self, user_name, email, password=None, **kwargs):
        """Create instance."""
        db.Model.__init__(self, user_name=user_name, email=email, **kwargs)
        if password:
            self.set_password(password)
        else:
            self.password = None

    def set_password(self, password):
        """Set password."""
        self.password = flask_bcrypt.generate_password_hash(password)

    def check_password(self, value):
        """Check password."""
        return flask_bcrypt.check_password_hash(self.password, value)

    @property
    def full_name(self):
        """Full user name."""
        return f"{self.first_name} {self.last_name}"

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<User({self.user_name!r})>"

    @staticmethod
    def encode_auth_token(user_id):
        """
        Expand to user_code->code factory
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                "exp": utc.shift(days=1).timestamp,
                "iat": utc.timestamp,
                "sub": user_id,
            }
            return jwt.encode(payload, SECRET_KEY, algorithm="HS256")
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, SECRET_KEY)
            is_blacklisted_token = BlacklistToken.check_blacklist(auth_token)
            if is_blacklisted_token:
                return "Token blacklisted. Please log in again."
            else:
                return payload["sub"]
        except jwt.ExpiredSignatureError:
            return "Signature expired. Please log in again."
        except jwt.InvalidTokenError:
            return "Invalid token. Please log in again."
