import uuid

from django.shortcuts import render, HttpResponseRedirect
from django.views import View
from django.contrib import messages

from cameras.models import Camera


class HomeView(View):
    template_name = "index.html"

    def get(self, request, data=None, *args, **kwargs):
        if request.user.is_authenticated:
            context = dict(user=request.user)
            if data == "cameras":
                self.template_name = "cameras.html"
                context['cameras'] = Camera.objects.all()
            return render(request, self.template_name, context=context)
        return render(request, 'login-form.html')


class AddCameraView(View):
    def post(self, request):
        is_success = False
        request_data = {k: v[0] for k, v in dict(request.POST).items() if k != 'csrfmiddlewaretoken'}
        try:
            uid = uuid.uuid4()
            Camera.objects.create(**request_data, uid=uid)
        except:
            messages.error(request, 'Грешка при добавяне на камера')

        if is_success:
            messages.success(request, 'Камерата е добавена успешно')

        return HttpResponseRedirect('/cameras/')
