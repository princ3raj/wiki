from django.urls import path

from . import views

from . import util

app_name = "encyclopedia"

urlpatterns = [
    path("", views.index, name="index"),
    path("newpage", views.newpage, name="create"),
    # Detail page for a single topic. 
    path('<str:entry_name>/', views.entry, name='entry'),
    path('random',views.randomfunction,name="random"),
    path('edit/<str:entry_title>/',views.edit,name="edit"),
  

]
