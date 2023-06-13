from rest_framework.views import APIView, Request, Response, status
from .serializers import UserSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserView(APIView):
    def post(self, request: Request) -> Response:
        user_data = request.data

        user_serializer = UserSerializer(data=user_data)

        user_serializer.is_valid(raise_exception=True)

        user_serializer.save()

        return Response(data=user_serializer.data, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    def post(self, request: Request) -> Response:
        login_serializer = TokenObtainPairSerializer(data=request.data)
        login_serializer.is_valid(raise_exception=True)

        return Response(data=login_serializer.validated_data, status=status.HTTP_200_OK)
