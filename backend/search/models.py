from django.db import models

# Create your models here.
from custom_user.models import User


class Search(models.Model):
    keyword = models.CharField(max_length=255, null=False)
    word = models.CharField(max_length=255, null=False)
    user_id = models.ForeignKey(User, null=False, on_delete=models.CASCADE)