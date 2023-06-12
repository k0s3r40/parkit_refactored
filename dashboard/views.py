from django.shortcuts import render
from django.views import View


class HomeView(View):
    template_name = "index.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            context = dict(user=request.user)

            return render(request, self.template_name, context=context)
        return render(request, 'login-form.html')
