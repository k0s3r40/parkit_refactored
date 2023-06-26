from django.urls import path

from dashboard.views import HomeView, AddCameraView

urlpatterns = [
    path('', HomeView.as_view()),
    path('<str:data>/', HomeView.as_view()),
    path('cameras/add/', AddCameraView.as_view())
]