from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project_name = models.TextField(max_length=50, default="")

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)
    endpoint = models.TextField(max_length=50, unique=True)
    async_func = models.BooleanField(default=0)
    async_result_url = models.URLField(default='https://uat.openapi.m-pesa.com/')
    async_result_time_delay = models.IntegerField(validators=[
            MinValueValidator(1)
        ], default=10)
    json_spec = models.TextField(default="[[{},{},200]]")
    connection_down = models.BooleanField(default=0)
    Intermittent_connection_issues = models.BooleanField(default=0)
    Intermittent_connection_per = models.IntegerField(validators=[
            MaxValueValidator(100),
            MinValueValidator(1)
        ], default=50)
    def __str__(self):
        return f'{self.user.username} Profile'
    result = models.TextField(default="")
    result_match = models.BooleanField(default=0)



