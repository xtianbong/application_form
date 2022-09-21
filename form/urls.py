from django.urls import path

from . import views
app_name="form"
urlpatterns=[
    path("",views.index, name='index'),
    path("completed",views.completed,name="completed")
]