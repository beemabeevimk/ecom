from django.db import models

# Create your models here.


class Database(models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField(max_length=30)
      