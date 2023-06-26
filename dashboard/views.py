import json
import uuid

from django.shortcuts import render, HttpResponseRedirect
from django.views import View
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

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

from django.utils.decorators import method_decorator

@method_decorator(csrf_exempt, name='dispatch')
class EditCameraView(View):
    template_name = 'edit_camera.html'

    def get(self, request, camera_uid, mask_type=False,  *args, **kwargs):
        context = {
            'camera': Camera.objects.get(uid=camera_uid)
        }

        if mask_type in ['parking', 'intruders']:
            self.template_name = 'camera_add_mask.html'
            context['mask_type'] = 'Паркинг' if mask_type == 'parking' else 'Нарушители'

        return render(request, self.template_name, context=context)


    def post(self, request, camera_uid, mask_type=False, *args, **kwargs):
        camera =  Camera.objects.get(uid=camera_uid)
        context = {
            'camera': camera
        }
        data = json.loads(request.body)
        if mask_type in ['parking', 'intruders']:
            self.template_name = 'camera_add_mask.html'
            context['mask_type'] = 'Паркинг' if mask_type == 'parking' else 'Нарушители'
            if mask_type == 'parking':
                camera.p_mask =data.get('polygons', [])
            else:
                camera.v_mask = data.get('polygons', [])
            camera.save()
            messages.success(request, 'Маската е добавена успешно')
        return render(request, self.template_name, context=context)