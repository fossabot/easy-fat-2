from django.forms import DateField, IntegerField, FloatField
from django.forms import ModelForm

from easyfat_ui.forms import EasyFatForm
from .models import Farm


class NewFarmForm(EasyFatForm, ModelForm):
    class Meta:
        model = Farm
        exclude = []