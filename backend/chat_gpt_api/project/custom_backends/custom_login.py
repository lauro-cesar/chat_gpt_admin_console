"""
"""
from django.contrib.auth.backends import BaseBackend
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
import uuid
import hashlib
import logging


logger = logging.getLogger(__name__)


User = get_user_model()


class CustomLogin(BaseBackend):
    """ """

    def hash_password(self, password):
        salt = uuid.uuid4().hex
        return (
            hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ":" + salt
        )

    def check_password(self, hashed_password, user_password):
        password, salt = hashed_password.split(":")

        p = hashlib.sha256(salt.encode() + user_password.encode()).hexdigest()

        return password == p

    def authenticate(self, request, username=None, password=None):
        # hashed_password = self.hash_password(username + password)
        try:
            tbuser = User.objects.get(user_code=username)
        except Exception as e:
            logger.error(e)
            return None
        else:
            if isinstance(tbuser, (User)):
                old_pass = password
                old_pass = username + old_pass
                if self.check_password(tbuser.password.strip(), old_pass):
                    try:
                        user = User.objects.get(username=username)
                    except User.DoesNotExist:
                        user = User(username=username, email=tbuser.email)
                        user.is_staff = True
                        user.is_superuser = False
                        user.save()
                        try:
                            grupo = Group.objects.get(name="operadores")
                        except Exception as e:
                            logger.error(e)
                            return None
                        else:
                            user.groups.set([grupo.pk])
                            user.save()
                    return user

        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
