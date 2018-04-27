from django.test import TestCase
from django.contrib.auth.models import User


class IndexViewInstantiationTest(TestCase):

    def setUp(self):
        User.objects.create_user('temporary', 'temporary@gmail.com', 'temporary')
        self.client.login(username='temporary', password='temporary')

    def test_instantiation(self):
        response = self.client.get('/')
        self.assertEqual('farm/index.html', response.template_name[0])
