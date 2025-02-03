# food_survey/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_page, name='main'),
    path('question1/', views.question1, name='question1'),
    path('question1/save/', views.save_question1, name='save_question1'),
    path('question2/', views.question2, name='question2'),
    path('question2/save/', views.save_question2, name='save_question2'),
    path('question3/', views.question3, name='question3'),
    path('question3/save/', views.save_question3, name='save_question3'),
    path('question4/', views.question4, name='question4'),
    path('question4/save/', views.save_question4, name='save_question4'),
    path('result/', views.result_page, name='result'),

]