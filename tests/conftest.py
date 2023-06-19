from app import app
import pytest

class TestBase:
    @classmethod
    def setup_class(cls):
        cls.app = app
        cls.api_call = app.test_client()
        cls.app_context = app.app_context()
        cls.app_context.push()

    @classmethod
    def teardown_class(cls):
        cls.app_context.pop()
