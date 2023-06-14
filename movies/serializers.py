from rest_framework import serializers
from movies.models import RatingsChoices, Movie, MovieOrder
from users.serializers import UserSerializer


class MovieSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=127)
    duration = serializers.CharField(max_length=10, allow_null=True, default=None)
    rating = serializers.ChoiceField(
        choices=RatingsChoices.choices, default=RatingsChoices.G
    )
    synopsis = serializers.CharField(allow_null=True, default=None)
    user = UserSerializer(write_only=True, allow_null=True, default=None)
    added_by = serializers.SerializerMethodField()

    def get_added_by(self, obj):
        return obj.user.email

    def create(self, validated_data: dict) -> Movie:
        return Movie.objects.create(**validated_data)


class MovieOrderSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    buyed_at = serializers.DateTimeField(read_only=True)
    price = serializers.DecimalField(max_digits=8, decimal_places=2)
    title = serializers.SerializerMethodField()
    buyed_by = serializers.SerializerMethodField()

    def get_title(self, obj):
        return obj.buyed_movie.title

    def get_buyed_by(self, obj):
        return obj.buyer.email

    def create(self, validated_data: MovieOrder):
        return MovieOrder.objects.create(**validated_data)
