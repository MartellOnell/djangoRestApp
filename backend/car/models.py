from django.db import models
from django.utils import timezone
import datetime


class Car(models.Model):
    user_id = models.IntegerField(default=1)
    company_name = models.CharField(max_length=30)
    model_name = models.CharField(max_length=50)
    content = models.TextField()
    pub_date = models.DateTimeField('date published', default=timezone.now)

    def __str__(self):
        return self.company_name

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class Comment(models.Model):
    user_id = models.IntegerField()
    car_id = models.IntegerField(default=1)
    rate = models.IntegerField(default=5)
    content = models.TextField()
    pub_date = models.DateTimeField('date published', default=timezone.now)

    cardel = models.ForeignKey(Car, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.rate)


class UnderComment(models.Model):
    user_id = models.IntegerField()
    comm_id = models.IntegerField()
    car_id = models.IntegerField(default=1)
    content = models.TextField()
    pub_date = models.DateTimeField('date published', default=timezone.now)

    comdel = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.comm_id)
    