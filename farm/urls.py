from django.conf.urls import url

from .views import FarmIndexView
from .wizards import NewFarmWizard


app_name = 'farm'
urlpatterns = [
    url(r'^$', FarmIndexView.as_view(), name='index'),
    url(r'^new_farm$', NewFarmWizard.as_view(), name='new_farm')
]