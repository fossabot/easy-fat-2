from .forms import EasyFatForm
from django.forms import CharField

from django.test import TestCase


class TestForm(EasyFatForm):
    field1 = CharField()
    field2 = CharField()


class TestEasyFatForm(TestCase):

    def setUp(self):
        self.form = TestForm()

    def test_attributes(self):
        self.assertEquals('form-control', self.form.fields['field1'].widget.attrs['class'])
        self.assertEquals('form-control', self.form.fields['field2'].widget.attrs['class'])
