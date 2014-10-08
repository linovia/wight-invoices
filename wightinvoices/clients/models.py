from django.db import models
from django.core.urlresolvers import reverse


class Client(models.Model):
    name = models.CharField(max_length=64)
    address = models.TextField(blank=True, null=True)

    # class Meta:
    #     unique_together = (
    #         ('name', 'site'),
    #     )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('client-detail', kwargs={'client_id': self.id})
