from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ChatsConfig(AppConfig):
    name = "chats"
    verbose_name = _("Chats")

    def ready(self):
        import chats.signals
