from django.urls import path
from item import views

urlpatterns = [
    path('items/',views.itemMaster.as_view(),name='item_list_create'),
    path('items/<int:item_id>/', views.itemMaster.as_view(), name='item_update_delete')
]