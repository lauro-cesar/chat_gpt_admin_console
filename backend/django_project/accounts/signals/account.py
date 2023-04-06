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
from accounts.models import Account


@receiver(pre_save, sender=Account)
def PreSaveAccountSignals(
        sender, instance, raw, using, update_fields, *args, **kwargs
):
    if hasattr(instance, "account_type"):
        print("oi")
        # print(instance.account_type.privilege_level)
    # set user previlegies based on account type


@receiver(post_save, sender=Account)
def PostSaveAccountSignals(
        sender, instance, created, using, update_fields, *args, **kwargs
):
    if True in [created]:
        for task in Account.TASKS.get("on_create", []):
            app.send_task(task, [instance.id])
    else:
        for task in Account.TASKS.get("on_save", []):
            app.send_task(task, [instance.id])
