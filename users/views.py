from rest_framework.views import APIView, Request, Response, status
from .serializers import UserSerializer


class UserView(APIView):
    def post(self, request: Request) -> Response:
        user_data = request.data

        user_serializer = UserSerializer(data=user_data)

        user_serializer.is_valid(raise_exception=True)

        user_serializer.save()

        return Response(data=user_serializer.data, status=status.HTTP_201_CREATED)
