from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import UserProfile


class UserProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'user/profile.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        profile = UserProfile.objects.get_profile_for_user(self.request.user)
        data.update({'bread_crumbs': ['User Profile', profile.username]})
        data.update({'profile': profile})
        data.update({'farms': self.__get_farm_data()})
        return data

    def __get_farm_data(self):
        user = self.request.user
        farm_relations = user.userfarmrelations_set.all()
        data = []
        for farm in farm_relations:
            if farm.relation == 'owner':
                data.append({'name': farm.farm.name, 'relation': '(co)owner'})
            else:
                data.append({'name': farm.farm.name, 'relation': farm.relation})
        return data
