from rest_framework.views import APIView, Request, Response, status
from .models import Movie
from .serializers import MovieSerializer, MovieOrderSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from users.permissions import AdminCustomPermission
from django.shortcuts import get_object_or_404


class MovieView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [AdminCustomPermission]

    def get(self, request: Request) -> Response:
        movies_list = Movie.objects.all()

        movie_serializer = MovieSerializer(instance=movies_list, many=True)

        return Response(data=movie_serializer.data, status=status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        validate_movie = MovieSerializer(data=request.data)

        validate_movie.is_valid(raise_exception=True)

        validate_movie.save(user=request.user)

        return Response(data=validate_movie.data, status=status.HTTP_201_CREATED)


class MovieDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [AdminCustomPermission]

    def get(self, request: Request, movie_id: int) -> Response:
        print(movie_id)
        movie_data = get_object_or_404(Movie, id=movie_id)

        movie_serializer = MovieSerializer(instance=movie_data)

        return Response(data=movie_serializer.data, status=status.HTTP_200_OK)

    def delete(self, request: Request, movie_id: int) -> Response:
        movie_data = get_object_or_404(Movie, id=movie_id)

        movie_data.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class MovieOrderView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request: Request, movie_id: int) -> Response:
        validated_movie_order = MovieOrderSerializer(data=request.data)

        validated_movie_order.is_valid(raise_exception=True)

        movie = get_object_or_404(Movie, id=movie_id)

        validated_movie_order.save(buyer=request.user, buyed_movie=movie)

        return Response(data=validated_movie_order.data, status=status.HTTP_201_CREATED)
