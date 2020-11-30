from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Queue(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    details = models.CharField(max_length=300, null=False, blank=False)
    location = models.CharField(max_length=20, null=False, blank=False)
    img = models.ImageField(upload_to='queues/', default='default-doctor.jpg')
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class QueuePosition(models.Model):
    queue = models.ForeignKey(Queue, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    timestamp = models.TimeField(auto_now=True)
    rank = models.IntegerField()

    def __str__(self):
        return str(self.user) + '-' + str(self.queue)

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rank = models.IntegerField()