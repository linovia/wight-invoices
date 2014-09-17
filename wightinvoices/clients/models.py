from django.db import models


class Client(models.Model):
    name = models.CharField(max_length=64)
    address = models.TextField(blank=True, null=True)

    # class Meta:
    #     unique_together = (
    #         ('name', 'site'),
    #     )

    def __str__(self):
        return self.name
