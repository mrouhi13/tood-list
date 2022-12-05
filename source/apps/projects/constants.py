from django.db import models
from django.utils.translation import gettext_lazy as _


class MemberRole(models.TextChoices):
    DEVELOPER = 'developer', _('Developer')
    MANAGER = 'manager', _('Manager')
