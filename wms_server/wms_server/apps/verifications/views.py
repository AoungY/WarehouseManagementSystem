import jwt
from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView

from wms_server.utils.utils import SQL

db = SQL()


class OrdinaryUserLoginView(APIView):
    def post(self, request, *args, **kwargs):
        # 获取用户名和密码
        username = request.data.get('username')
        password = request.data.get('password')

        user = db.get_user(username, password)
        print(user)
        if not user:
            return Response({"error": "用户名或密码错误"}, status=400)
        payload = {'username': username}
        # 生成JWT token
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        return Response({'token': token})
