from django.shortcuts import render
from django.views import View


class HomeView(View):
    template_name = "home.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return render(request, self.template_name)
        return render(request, 'login-form.html')
