import base64
import hashlib

import jwt
from cryptography.fernet import Fernet
from django.conf import settings
from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed


class SimpleUser:
    """
    一个简单的用户类，只有一个is_authenticated属性,用于JWT认证
    """

    def __init__(self, payload):
        self.payload = payload

    @property
    def is_authenticated(self):
        return True


class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        token = request.headers.get('Authorization')

        if not token:
            return None
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('token已过期')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('无效的token')

        # 返回一个SimpleUser实例和None
        return (SimpleUser(payload), None)


# 从Django的SECRET_KEY生成Fernet密钥
def generate_fernet_key(secret_key):
    # 使用SHA-256哈希算法，确保密钥长度符合要求
    hash_key = hashlib.sha256(secret_key.encode()).digest()
    # 转换为base64编码以符合Fernet密钥格式
    return base64.urlsafe_b64encode(hash_key)
