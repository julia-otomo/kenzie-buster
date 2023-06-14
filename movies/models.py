from django.db import models


class RatingsChoices(models.TextChoices):
    G = "G"
    PG = "PG"
    PG13 = "PG-13"
    R = "R"
    NC17 = "NC-17"


class Movie(models.Model):
    title = models.CharField(max_length=127)
    duration = models.CharField(max_length=10, null=True, default=None)
    rating = models.CharField(
        max_length=20, choices=RatingsChoices.choices, default=RatingsChoices.G
    )
    synopsis = models.TextField(null=True, default=None)
    user = models.ForeignKey(
        "users.User", related_name="movies", on_delete=models.CASCADE
    )
    buyers = models.ManyToManyField(
        "users.User", through="MovieOrder", related_name="buyed_movies"
    )


class MovieOrder(models.Model):
    buyer = models.ForeignKey("users.User", on_delete=models.CASCADE)
    buyed_movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    buyed_at = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
