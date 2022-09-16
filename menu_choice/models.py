from django.db import models
from restaurant import settings


class Restaurant(models.Model):

    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Menu(models.Model):
    WEEK_DAYS = [
        ("Monday", "Mon",),
        ("Tuesday", "Tue",),
        ("Wednesday", "Wed"),
        ("Thursday", "Thu"),
        ("Friday", "Fri"),
        ("Saturday", "Sat"),
        ("Sunday", "Sun"),
    ]

    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    day = models.CharField(max_length=50, choices=WEEK_DAYS)
    content = models.TextField()

    class Meta:
        unique_together = ("restaurant", "day")

    def __str__(self):
        return f"{self.day}, {self.restaurant}, {self.content}"

    @property
    def votes_count(self):
        return self.vote_set.all().count()


class Vote(models.Model):

    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True
    )

    class Meta:
        unique_together = ("menu", "user")

    def __str__(self):
        return f"{self.menu}, {self.user}"
