from django.urls import path
from . import views

urlpatterns = [ 

    path('', views.question_1, name="question"),

]
