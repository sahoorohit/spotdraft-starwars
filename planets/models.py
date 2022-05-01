from django.db import models

from utils.models import CustomBaseModel


class Planet(CustomBaseModel):

    name = models.CharField(max_length=50)
    is_favorite = models.BooleanField(default=False)

    custom_name = models.CharField(max_length=50, null=True)

    def __str__(self):
        return "{}".format(self.name)
