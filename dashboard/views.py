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
            context['dashboard_data'] = {
                'total_parked': sum([i.current_cap for i in Camera.objects.all()]),
                'max_cap': sum([i.max_cap for i in Camera.objects.all()]),
                'intruders': sum([i.intruders_count for i in Camera.objects.all()]),

            }
            context['dashboard_data']['taken_percentage'] = round((context['dashboard_data']['total_parked'] / context['dashboard_data']['max_cap']) * 100, 2)

            green_parked = sum([i.current_cap for i in Camera.objects.filter(zone='green')])
            blue_parked = sum([i.current_cap for i in Camera.objects.filter(zone='blue')])

            total_parked = green_parked + blue_parked

            green_ratio = round((green_parked / total_parked) * 100, 2)
            blue_ratio = round((blue_parked / total_parked) * 100, 2)

            context['dashboard_data']['green_ratio'] = green_ratio
            context['dashboard_data']['blue_ratio'] = blue_ratio

            green_intruders = sum([i.intruders_count for i in Camera.objects.filter(zone='green')])
            blue_intruders = sum([i.intruders_count for i in Camera.objects.filter(zone='blue')])
            total_intruders = green_intruders + blue_intruders

            green_ratio_int = round((green_intruders / total_intruders) * 100, 2)
            blue_ratio_int = round((blue_intruders / total_intruders) * 100, 2)

            context['dashboard_data']['green_ratio_int'] = green_ratio_int
            context['dashboard_data']['blue_ratio_int'] = blue_ratio_int
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

    def get(self, request, camera_uid, mask_type=False, *args, **kwargs):
        context = {
            'camera': Camera.objects.get(uid=camera_uid)
        }

        if mask_type in ['parking', 'intruders']:
            self.template_name = 'camera_add_mask.html'
            context['mask_type'] = 'Паркинг' if mask_type == 'parking' else 'Нарушители'

        return render(request, self.template_name, context=context)

    def post(self, request, camera_uid, mask_type=False, *args, **kwargs):
        camera = Camera.objects.get(uid=camera_uid)
        context = {
            'camera': camera
        }
        data = json.loads(request.body)
        if mask_type in ['parking', 'intruders']:
            self.template_name = 'camera_add_mask.html'
            context['mask_type'] = 'Паркинг' if mask_type == 'parking' else 'Нарушители'
            if mask_type == 'parking':
                camera.p_mask = data.get('polygons', [])
            else:
                camera.v_mask = data.get('polygons', [])
            camera.height = data.get('height')
            camera.width = data.get('width')
            print(camera.height)
            print(camera.width)
            camera.save()
            messages.success(request, 'Маската е добавена успешно')
        return render(request, self.template_name, context=context)
