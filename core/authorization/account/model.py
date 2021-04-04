from sqlalchemy import Column, String
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt, InvalidKey
from os import urandom

from core.base.model import BaseModel
# from core.cache.redis_cache.decorate import redis_cache
from libs.error import KEY_NOT_FOUND, PASSWORD_ILLEGAL


class Account(BaseModel):
    __tablename__ = 'account'

    account = Column(String(20), doc='账号', nullable=False)
    salt = Column(String(16), doc='加盐', nullable=False)
    password = Column(String(128), doc='加密后的密码', nullable=False)  # PBKDF2、bcrypt、scrypt
    status = Column(String(10), doc='账号状态', nullable=False, default='active')  # active 活跃

    @classmethod
    def encrypt(cls, info):
        if 'password' not in info:
            raise KEY_NOT_FOUND.description('请输入密码')

        password = info['password']
        salt = urandom(16)
        kdf = Scrypt(
            salt=salt,
            length=32,
            n=2 ** 14,
            r=8,
            p=1,
        )
        encrypted_password = kdf.derive(password.encode())
        info['password'] = encrypted_password
        info['salt'] = salt

    @classmethod
    def verify(cls, info, password):
        if 'password' not in info or 'salt' not in info:
            raise KEY_NOT_FOUND.description('请输入密码')

        salt = info['salt']
        kdf = Scrypt(
            salt=salt,
            length=32,
            n=2 ** 14,
            r=8,
            p=1,
        )
        encrypted_password = info['password']

        try:
            kdf.verify(password.encode(), encrypted_password)
        except InvalidKey:
            raise PASSWORD_ILLEGAL.description('请输入正确的密码')
