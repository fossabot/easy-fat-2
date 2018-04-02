from django.views.generic import TemplateView


class FarmIndexView(TemplateView):
    template_name = "farm/index.html"
