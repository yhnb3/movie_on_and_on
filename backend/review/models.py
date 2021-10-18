from django.db import models
from django.contrib import admin
from custom_user.models import User
from movie.models import Movie

# Create your models here.
class Review(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User,to_field='email', on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    title = models.CharField(max_length=300, null=False)
    body = models.TextField(null=False)

    class Meta:
        db_table = "Review"




admin.site.register(Review)
