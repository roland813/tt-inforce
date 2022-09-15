from django.db import models, IntegrityError


class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    votes = models.IntegerField(default=0)

    menu_monday = models.TextField(
        blank=True,
    )
    menu_tuesday = models.TextField(
        blank=True,
    )
    menu_wednesday = models.TextField(
        blank=True,
    )
    menu_thursday = models.TextField(
        blank=True,
    )
    menu_friday = models.TextField(
        blank=True,
    )
    menu_saturday = models.TextField(
        blank=True,
    )
    menu_sunday = models.TextField(
        blank=True,
    )


class Vote(models.Model):
    restaurant = models.ForeignKey(
        to=Restaurant,
        on_delete=models.CASCADE,
        related_name='vote'
    )

    def save(self, commit=True, *args, **kwargs):
        if commit:
            try:
                self.restaurant.votes += 1
                self.restaurant.save()
                super(Vote, self).save(*args, **kwargs)

            except IntegrityError:
                self.restaurant.votes -= 1
                self.restaurant.save()
                raise IntegrityError
        else:
            raise IntegrityError
