from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class FarmIndexView(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        kpi_info = {'color': 'primary',
                    'icon': 'bug',
                    'value': '512',
                    'description': 'Animals in the farm',
                    'action': '#',
                    'action_name': 'View Details'}
        data.update({'kpi_info': kpi_info})
        data.update({'bread_crumbs': ['Dashboard']})

        return data

    template_name = "farm/index.html"
