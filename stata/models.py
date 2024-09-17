from django.db import models


# Create your models here.
class Activities(models.Model):
    activity_id = models.BigIntegerField(unique=True)
    name = models.CharField(max_length=255, null=False, blank=False)
    distance = models.FloatField()
    elevation = models.IntegerField()
    moving_time = models.DurationField()
    average_speed = models.FloatField(null=True)
    average_watts = models.FloatField(null=True)
    ride_type = models.CharField(max_length=255, null=False, blank=False)
    date = models.DateTimeField()
    location = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.activity_id} - {self.name} - {self.date}'
