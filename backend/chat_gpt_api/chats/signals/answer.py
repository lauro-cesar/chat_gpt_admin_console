
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
from chats.models import Answer


@receiver(post_save, sender=Answer)
def PostSaveAnswerSignals(
    sender, instance, created, using, update_fields, *args, **kwargs
):
    if True in [created]:
        for task in Answer.TASKS.get('on_create',[]):
            app.send_task(task, [instance.id])
    else:
        for task in Answer.TASKS.get('on_save',[]):
            app.send_task(task, [instance.id])