from django.conf.urls import url

from .views import UserProfileView


app_name = 'accounts'

urlpatterns = [
    url(r'^profile$', UserProfileView.as_view(), name='index'),
]