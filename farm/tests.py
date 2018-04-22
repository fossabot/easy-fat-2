from django.test import TestCase


class IndexViewInstantiationTest(TestCase):
    def test_instantiation(self):
        response = self.client.get('/')
        self.assertEqual('farm/index.html', response.template_name[0])
