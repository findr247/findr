from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('items', views.items_list, name='items'),
    path('items/<int:item_id>', views.item_details, name="item_details")
]