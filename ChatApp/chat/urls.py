from django.urls import path, include
from chat import views as chat_views
from django.contrib.auth.views import LoginView, LogoutView


from django.urls import path

from . import views
urlpatterns = [
    path('', views.index, name='home'),
    path('ticket_details/<int:id>/', views.ticket_details, name='ticket_details'),
    path('staff/login/', views.staff_login, name='staff_login'),
    path('staff/dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path('assign_ticket/<int:ticket_id>/', views.assign_ticket, name='assign_ticket'),
    path('staff/create/', views.staff_create, name='staff_create'),
]


