from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from .views import FarmIndexView


app_name = 'farm'
urlpatterns = [
    url(r'^$', FarmIndexView.as_view(), name='index'),
]