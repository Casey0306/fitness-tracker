from django.db import models
from users.models import User
from django.utils import timezone


class Acttype(models.Model):
    type_name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(editable=False)
    updated_at = models.DateTimeField()

    def __str__(self):
        return self.type_name

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super(Acttype, self).save(*args, **kwargs)


class Fitstat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(editable=False)
    updated_at = models.DateTimeField()
    start_time = models.DateTimeField()
    stop_time = models.DateTimeField()
    type_of_activity = models.ForeignKey(Acttype, on_delete=models.CASCADE)
    distance = models.IntegerField()
    calories = models.IntegerField()

    def __str__(self):
        return f'{[self.distance, self.calories]!r}'

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super(Fitstat, self).save(*args, **kwargs)
