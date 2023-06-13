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
