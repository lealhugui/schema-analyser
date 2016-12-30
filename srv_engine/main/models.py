from django.db import models
from srv_engine.models import Model

class Person(Model):
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)

    def __str__(self):
        return "{f} {l}".format(f=self.first_name, l=self.last_name)
