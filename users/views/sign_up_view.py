from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from users.serializer.user_serializer import UserSerializer


class SignUpView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        data = request.data
        serializer = UserSerializer(data=request.data)
        # dict(
        #     phone_number=data.get("phone_number"),
        #     first_name=data.get("first_name"),
        #     last_name=data.get("last_name"),
        #     password=data.get("password"),
        #     # confirm_password=data.get("confirm_password")
        # ))
        if serializer.is_valid():
            serializer.save()
            return Response()
        return Response(serializer.errors, status=404)
