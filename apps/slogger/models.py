from django.db import models
from django.core.urlresolvers import reverse
from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import ugettext as _

from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User

from autoslug.fields import AutoSlugField

class Slog(models.Model):
    """Contains the slug name & object id """
    content_type = models.ForeignKey(ContentType)
    object_id = models.CharField(max_length=255)
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    objname = models.CharField(max_length=255)
    slugname = AutoSlugField(populate_from='objname',unique_with='objname',editable=True)
