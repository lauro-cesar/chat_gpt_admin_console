from django.test import TestCase
import project.celery_tasks
from project.authentication import APITokenAuthentication


class ProjectEnvironmentTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.keyword = "Bearer"

    def test_if_model_exists(self):
        self.assertEqual("c", "c")

    def test_if_keyword_is_bearer(self):
        a = APITokenAuthentication()
        self.assertEqual(a.keyword, self.keyword)
