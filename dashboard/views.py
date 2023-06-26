from django.shortcuts import render, HttpResponseRedirect
from django.views import View
from django.contrib import messages

class HomeView(View):
    template_name = "index.html"

    def get(self, request,data=None, *args, **kwargs):
        if request.user.is_authenticated:
            context = dict(user=request.user)
            if data == "cameras":
                self.template_name = "cameras.html"

            return render(request, self.template_name, context=context)
        return render(request, 'login-form.html')


class AddCameraView(View):
    def post(self, request):
        print(request.POST)
        messages.success(request, 'Camera added successfully.')
        return HttpResponseRedirect('/cameras/')