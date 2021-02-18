from django.urls import path

from . import views

app_name = 'gallery'

urlpatterns = [
    path('', views.image_list, name='list'),
    path('<int:image_id>/', views.image_detail, name='detail'),
    path('add/', views.image_add, name='add'),
]
