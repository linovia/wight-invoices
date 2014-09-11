from django.db import models
from django.contrib.sites.models import Site


class Client(models.Model):
    name = models.CharField(max_length=64)
    address = models.TextField()
    site = models.ForeignKey(Site)

    class Meta:
        unique_together = (
            ('name', 'site'),
        )

    def __str__(self):
        return self.name
