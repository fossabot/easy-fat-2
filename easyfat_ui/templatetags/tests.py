from django.test import TestCase
from django.template import Template, Context


class KpiCallTestCase(TestCase):
    TEMPLATE = Template("{% load kpi %} {% kpi kpi_info %}")
    kpi_info = {'color': 'primary',
                'icon': 'bug',
                'value': '512',
                'description': 'Animals in the farm',
                'action': '#',
                'action_name': 'View Details'}

    def test_instantiation(self):
        self.TEMPLATE.render(Context({'kpi_info': self.kpi_info}))
