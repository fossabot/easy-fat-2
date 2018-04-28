from easyfat_ui.views import EasyFatWizardView

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse

from .forms import NewFarmForm


class NewFarmWizard(LoginRequiredMixin, EasyFatWizardView):
    wizard_name = 'New farm'
    form_list = [('farm_info', NewFarmForm)]

    title_dict = {'farm_info': 'General Farm Information'}

    def done(self, form_list, **kwargs):
        return HttpResponseRedirect(reverse('farm:index'))

    def get_context_data(self, form, **kwargs):
        data = super().get_context_data(form, **kwargs)
        data.update({'bread_crumbs': ['Farm Wizards', 'New Farm']})
        return data

