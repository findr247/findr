from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    # path('upload', views.upload, name='upload'),
    path('signup/', views.signup_view, name='signup'),
    path('signin/', views.signin_view, name='signin'),
    path('profile/', views.profile, name="profile"),
    path('report/', views.report_item, name='report'),
    path('report/<int:item_id>', views.report_item, name='report_id'),
    path('claim/<int:item_id>', views.claim_item, name='claim'),
    path('download-backup/', views.download_db_and_media, name='download_backup'),
    path('items', views.items, name='items_'),
    path('items/<int:item_id>', views.item_details, name='item_details'),
    path('new/', views.new),
    path('events/', views.cse_view)
]
