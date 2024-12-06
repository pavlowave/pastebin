from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_paste, name='create_paste'),
    path('<slug:slug>/', views.get_paste, name='get_paste'),
]