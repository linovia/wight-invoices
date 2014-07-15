from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import smart_text
from django.utils.encoding import python_2_unicode_compatible



@python_2_unicode_compatible
class History(models.Model):
    action_time = models.DateTimeField(_('action time'), auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    # Used for the invoice or estimate
    content_type = models.ForeignKey(ContentType, blank=True, null=True)
    object_id = models.TextField(_('object id'), blank=True, null=True)
    object_repr = models.CharField(_('object repr'), max_length=200)

    # What happened
    action = models.CharField(_('action flag'), max_length=32)

    class Meta:
        verbose_name = _('history')
        ordering = ('-action_time',)

    def __repr__(self):
        return smart_text(self.action_time)

    def __str__(self):
        return "%s %s %s at %s" % (self.user, self.action, self.object_repr, self.action_time)
