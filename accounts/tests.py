from django.test import TestCase
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
import django.db
import django.db.transaction

# Create your tests here.
# TDD - test driven development
"""
SERIALIZE DATA INTO A FIXTURE
USE FIXTURES TO SIMPLIFY TEST DATA
It's json data that the test can load
"""
RAW_PASSWORD = 'mypassword'
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


class UserPasswordTests(TestCase):
    def tearDown(self) -> None:
        # print passwords as stored in test database
        for user in User.objects.all():
            print(f'username: {user.username}\tpassword: {user.password}')

    def test_user_create_missing_required_fields(self):
        # none of these raise any exceptions, despite required model fields
        user_kwargs = [dict(),
                       dict(username='a'),
                       dict(username='b', password=''),
                       dict(username='c', password=RAW_PASSWORD)]
        for kwargs in user_kwargs:
            user = User.objects.create(**kwargs)
            # password is "usable" ...
            self.assertTrue(user.has_usable_password())
            if 'password' in kwargs:
                # stored password is still raw (not hashed)
                self.assertEqual(kwargs['password'], user.password)
                # ... but password-check fails
                self.assertFalse(user.check_password(kwargs['password']))

    def test_user_set_password(self):
        # can set a usable password after user creation
        user = User(username='d')
        user.set_password(RAW_PASSWORD)  # does not save...
        user.save()
        self.assertTrue(user.has_usable_password())
        self.assertNotEqual(RAW_PASSWORD, user.password)
        self.assertTrue(user.check_password(RAW_PASSWORD))

    def test_user_create_hashed_password(self):
        # we can initialize with a hashed password
        hashed_password = make_password(RAW_PASSWORD)
        user = User.objects.create(username='e', password=hashed_password)
        self.assertTrue(user.has_usable_password())
        self.assertTrue(user.check_password(RAW_PASSWORD))

    def test_user_set_unusable_password(self):
        # can set an unusable password
        user = User(username='f')
        user.set_unusable_password()  # does not save...
        user.save()
        self.assertFalse(user.has_usable_password())

    @django.db.transaction.atomic
    def test_user_create_password_none(self):
        # cannot initialize with password=None (violates the NOT NULL constraint)
        with self.assertRaises(django.db.IntegrityError) as a:
            User.objects.create(username='g', password=None)
        self.assertIn('not null', str(a.exception).lower())

    def test_user_set_password_none(self):
        # can set None in set_password(), but that becomes unusable
        user = User(username='h')
        user.set_password(None)
        user.save()
        self.assertFalse(user.has_usable_password())
