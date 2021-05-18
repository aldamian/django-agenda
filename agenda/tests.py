from django.contrib.auth import get_user_model
from django.test import TestCase

# Create your tests here.
from .models import Agenda

User = get_user_model()


class AgendaTestCase(TestCase):

    def setUp(self):
        user_a_name = 'test_user'
        user_a_email = 'test_user@email.com'
        user_a_pw = 'password1234'

        self.user_a_name = user_a_name
        self.user_a_pw = user_a_pw
        self.user_a_email = user_a_email

        user_a = User(username=user_a_name, email=user_a_email)

        user_a.is_staff = True
        user_a.is_superuser = False
        user_a.set_password(user_a_pw)
        user_a.save()
        self.user_a = user_a

        user_b = User.objects.create_user('user_2', 'email@invalid.com', 'something_password')
        self.user_b = user_b

    def test_user_count(self):
        user_count = User.objects.all().count()
        self.assertEqual(user_count, 2)

    def test_agenda_create(self):
        self.client.login(username=self.user_b.username,
                          password='something_password')
        response = self.client.post("/agenda/create/",
                                    {"title": "this is a valid test",
                                     "tags": "test",
                                     "content": "This is the content of the test"})
        self.assertEqual(response.status_code, 200)

    def test_invalid_request(self):
        self.client.login(username=self.user_b.username,
                          password='something_password')
        response = self.client.get("/agenda/")
        self.assertNotEqual(response.status_code, 200)

    def test_valid_request(self):
        self.client.login(username=self.user_a.username,
                          password='password1234')
        response = self.client.get("/agenda/")
        self.assertTrue(response.status_code, 200)
