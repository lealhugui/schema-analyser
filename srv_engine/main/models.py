from srv_engine import models
from django.contrib.auth.models import User as AuthUser


class User(AuthUser, models.GQLModel):
    """Proxy model, just to expose the model to the GQL interface"""
    class Meta:
        proxy = True


class Feature(models.GQLModel):
    """System Features"""
    name = models.TextField(max_length=120)
    description = models.TextField(max_length=120)
    url = models.TextField(max_length=120)