from django.db import models
from django.contrib.auth.models import User


class GameHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField()
    played_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.score}'


class Achievement(models.Model):
    title = models.CharField(max_length=100)
    threshold_score = models.IntegerField()

    def __str__(self):
        return self.title
