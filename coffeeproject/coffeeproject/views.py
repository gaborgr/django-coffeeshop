from django.shortcuts import render
from django.views.generic import TemplateView


def home(request):
    return render(request, "home.html")


class AboutView(TemplateView):
    template_name = "about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["project_tech"] = {
            "database": "PostgreSQL",
            "env_manager": "python-dotenv",
        }
        return context
