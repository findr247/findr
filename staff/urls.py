from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('users', views.users, name='users'),
    path('items', views.items_list, name='items'),
    path('items/<int:item_id>', views.item_details, name="item_details"),
    path('items/claimed/<int:claim_id>', views.item_claimed, name="claim_details")
]