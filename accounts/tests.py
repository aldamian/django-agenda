from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase

# Create your tests here.
# TDD - test driven development
"""
SERIALIZE DATA INTO A FIXTURE
USE FIXTURES TO SIMPLIFY TEST DATA
It's json data that the test can load
"""
User = get_user_model()


class UserTestCase(TestCase):

    def setUp(self):

        user_a_name = 'test_user'
        user_a_email = 'test_user@email.com'
        user_a_pw = 'password1234'

        self.user_a_name = user_a_name
        self.user_a_pw = user_a_pw
        self.user_a_email = user_a_email

        user_a = User(username=user_a_name, email=user_a_email)

        user_a.is_staff = True
        user_a.is_superuser = True
        user_a.set_password(user_a_pw)
        user_a.save()
        self.user_a = user_a

    def test_user_exists(self):
        user_count = User.objects.all().count()
        self.assertEqual(user_count, 1)
        self.assertNotEqual(user_count, 0)

    # def test_user_password(self):
    #     self.assertTrue(self.user_a.check_password(self.user_a_pw))

    def test_user_password(self):
        user_a = User.objects.get(username="test_user")
        self.assertTrue(
            user_a.check_password(self.user_a_pw)
        )

    def test_login_url(self):
        login_url = settings.LOGIN_URL
        # python requests - manage.py runserver
        # self.client.get, self.client.post
        data = {"username": self.user_a_name, "password": self.user_a_pw}
        response = self.client.post(login_url, data, follow=True)
        # print(dir(response))
        # print(response.request))
        status_code = response.status_code
        redirect_path = response.request.get("PATH_INFO")
        self.assertEqual(redirect_path, settings.LOGIN_REDIRECT_URL)  # the redirect isn't happening
        self.assertEqual(status_code, 200)
