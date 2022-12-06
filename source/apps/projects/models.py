from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.projects.constants import MemberRole
from core.models import AbstractBaseModel

User = get_user_model()


class Project(AbstractBaseModel):
    members = models.ManyToManyField(
        verbose_name=_('Members'),
        to=User,
        related_name='projects',
        through='Member'
    )
    title = models.CharField(
        verbose_name=_('Title'),
        max_length=60,
    )

    class Meta:
        verbose_name = _('Project')
        verbose_name_plural = _('Projects')

    def __str__(self):
        return self.title


class Member(AbstractBaseModel):
    user = models.ForeignKey(
        verbose_name=_('User'),
        to=User,
        related_name='members',
        on_delete=models.CASCADE,
    )
    project = models.ForeignKey(
        verbose_name=_('Project'),
        to='Project',
        related_name='members_set',
        on_delete=models.PROTECT,
    )
    role = models.CharField(
        verbose_name=_('Role'),
        max_length=20,
        choices=MemberRole.choices,
        default=MemberRole.DEVELOPER,
    )

    class Meta:
        verbose_name = _('Member')
        verbose_name_plural = _('Members')
        unique_together = ['user', 'project']

    def __str__(self):
        return f'{self.user.__str__()} - {self.project.__str__()}'
