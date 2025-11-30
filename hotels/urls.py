from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('hotel/<int:pk>/', views.hotel_detail, name='hotel_detail'),
    path('add/', views.add_hotel, name='add_hotel'),
    path('edit/<int:pk>/', views.edit_hotel, name='edit_hotel'),
    path('delete/<int:pk>/', views.delete_hotel, name='delete_hotel'),
    path('my-hotels/', views.my_hotels, name='my_hotels'),
    path('signup/', views.signup, name='signup'),
]