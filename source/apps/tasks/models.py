from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import AbstractBaseModel


class Task(AbstractBaseModel):
    project = models.ForeignKey(
        verbose_name=_('Project'),
        to='projects.Project',
        related_name='tasks',
        on_delete=models.CASCADE,
    )
    assignees = models.ManyToManyField(
        verbose_name=_('Assignees'),
        to='projects.Member',
        related_name='tasks',
        blank=True,
    )
    title = models.CharField(
        verbose_name=_('Title'),
        max_length=100,
    )
    description = models.TextField(
        verbose_name=_('Description'),
        blank=True,
    )

    class Meta:
        verbose_name = _('Task')
        verbose_name_plural = _('Tasks')

    def __str__(self):
        return self.title
