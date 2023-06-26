from django.urls import path

from dashboard.views import HomeView, AddCameraView, EditCameraView

urlpatterns = [
    path('', HomeView.as_view()),
    path('<str:data>/', HomeView.as_view()),
    path('cameras/add/', AddCameraView.as_view()),
    path('cameras/<str:camera_uid>/', EditCameraView.as_view(), name='edit-camera'),
    path('cameras/<str:camera_uid>/<str:mask_type>/', EditCameraView.as_view(), name='add-mask')
]