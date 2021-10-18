from django.db import models
from django.contrib import admin
from custom_user.models import User
# Create your models here.


class Board(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.IntegerField(null=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=300, null=False)
    content = models.CharField(max_length=1500, null=False)
    reg_time = models.DateTimeField(auto_now=True)
    update_time = models.DateTimeField(null=True)

    class Meta:
        db_table = "Board"




admin.site.register(Board)
