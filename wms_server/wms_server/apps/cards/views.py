from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView

from verifications.utils import JWTAuthentication
from wms_server.utils.utils import SQL

db = SQL()


class CardsView(APIView):
    # 需要登录
    # 只在这里声明验证类，不全局应用权限
    authentication_classes = [JWTAuthentication]

    # permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # 从query中获取card_id
        card = request.query_params.get('card')
        if not card:
            return Response({"error": "缺少必要的参数card"}, status=400)
        # 从数据库中查找该卡号对应的信息
        card_info = db.get_card(card)
        if not card_info:
            return Response({"error": "该卡暂未注册"}, status=400)
        return Response(card_info)

    def post(self, request, *args, **kwargs):
        # 在post方法中检查用户是否认证
        if not request.user.is_authenticated:
            raise PermissionDenied("用户未认证，无法进行此操作")

        required_fields = ['id', 'is_borrowed', 'name', 'origin', 'storage_location', 'inventory', 'card_number']
        # 从request中获取数据
        data = request.data
        # 检查数据是否完整
        for field in required_fields:
            if field not in data:
                return Response({"error": f"缺少必要的参数{field}"}, status=400)

        flag = db.update_card(data)
        if flag:
            return Response({"message": "更新成功"}, status=200)
        else:
            return Response({"error": "未知错误"}, status=400)

    def delete(self, request, *args, **kwargs):
        # 在delete方法中检查用户是否认证
        if not request.user.is_authenticated:
            raise PermissionDenied("用户未认证，无法进行此操作")

        card = request.query_params.get('card')
        if not card:
            return Response({"error": "缺少必要的参数card"}, status=400)
        flag = db.delete_card(card)
        if flag:
            return Response({"message": "删除成功"}, status=200)
        else:
            return Response({"error": "未知错误"}, status=400)
