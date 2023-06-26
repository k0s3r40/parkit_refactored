from django.urls import path

from dashboard.views import HomeView

urlpatterns = [
    path('', HomeView.as_view()),
    path('<str:data>/', HomeView.as_view())
]