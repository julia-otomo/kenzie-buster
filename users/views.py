from rest_framework.views import APIView, Request, Response, status

from users.models import User
from .serializers import UserSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAdminUser
from users.permissions import IsOwnerPermission
from django.shortcuts import get_object_or_404


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


class UserDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsOwnerPermission]

    def get(self, request: Request, user_id: int) -> Response:
        user = get_object_or_404(User, id=user_id)

        self.check_object_permissions(request, user)

        user_serializer = UserSerializer(instance=user)

        return Response(data=user_serializer.data, status=status.HTTP_200_OK)

    def patch(self, request: Request, user_id: int) -> Response:
        user = get_object_or_404(User, id=user_id)

        self.check_object_permissions(request, user)

        user_serializer = UserSerializer(instance=user, data=request.data, partial=True)

        user_serializer.is_valid(raise_exception=True)

        user_serializer.save()

        return Response(data=user_serializer.data, status=status.HTTP_200_OK)
