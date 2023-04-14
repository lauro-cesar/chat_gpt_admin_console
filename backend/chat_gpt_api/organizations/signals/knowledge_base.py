
"""
Copyright (c) 2023, Lauro Cesar <lauro@hostcert.com.br>
All rights reserved under BSD 3-Clause License.
"""

from django.db.models.signals import (
    pre_save,
    post_save,
    pre_init,
    post_init,
    pre_delete,
    post_delete,
    m2m_changed,
)

import hashlib
from django.dispatch import receiver
from django.conf import settings
from project.celery_tasks import app
from organizations.models import KnowledgeBase


@receiver(post_save, sender=KnowledgeBase)
def PostSaveKnowledgeBaseSignals(
    sender, instance, created, using, update_fields, *args, **kwargs
):
    if True in [created]:
        for task in KnowledgeBase.TASKS.get('on_create',[]):
            app.send_task(task, [instance.id])
    else:
        for task in KnowledgeBase.TASKS.get('on_save',[]):
            app.send_task(task, [instance.id])