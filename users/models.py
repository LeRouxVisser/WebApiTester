from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    endpoint = models.TextField(max_length=50, unique=True)
    json_spec = models.TextField(default="[[{},{},200]]")
    connection_down = models.BooleanField(default=0)
    Intermittent_connection_issues = models.BooleanField(default=0)
    Intermittent_connection_per = models.IntegerField(validators=[
            MaxValueValidator(100),
            MinValueValidator(1)
        ], default=50)
    def __str__(self):
        return f'{self.user.username} Profile'


