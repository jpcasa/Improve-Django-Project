from django.urls import path
from . import views

app_name = 'menu'

urlpatterns = [
    path('', views.menu_list, name='menu_list'),
    path('menu/<int:pk>/edit/', views.edit_menu, name='menu_edit'),
    path('menu/<int:pk>/', views.menu_detail, name='menu_detail'),
    path('menu/item/<int:pk>/', views.item_detail, name='item_detail'),
    path('menu/new/', views.create_new_menu, name='menu_new'),
]
