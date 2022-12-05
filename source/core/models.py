from django.db import models
from django.utils.translation import gettext_lazy as _


class AbstractBaseModel(models.Model):
    updated_at = models.DateTimeField(
        verbose_name=_('Updated at'),
        auto_now=True,
    )
    created_at = models.DateTimeField(
        verbose_name=_('Created at'),
        auto_now_add=True,
    )

    class Meta:
        abstract = True
