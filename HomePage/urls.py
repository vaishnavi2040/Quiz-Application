"""online_quiz URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from unicodedata import name
from django.contrib import admin
from django.urls import path

from rest_framework import routers
from .views import student_delete, student_edit,student_update,ResultList,feedbackList,quizListStaff,quiz_add,quiz_edit,quiz_update,quiz_delete,questionListStaff,question_edit,question_update,question_delete
from .views import QuizListView, log_in_staff,log_out_staff,log_in,log_out,index,quiz_View,quiz_data_view,save_quiz_view,feedback_view,save_feedback_view,quiz_List,staff_home,studentList,student_add,delete_answer,QuestionUpdate,QuestionCreate
from django.views.generic.base import TemplateView # Add this

#question_add,


urlpatterns = [
    
    path("",index,name="index"),
    # path("Student Login/",login_student, name='login'),
    path("Login/", log_in, name='login'),
    path('logout/', log_out, name='logout'),
    path('dashboard_student/',quiz_List,name ="main-view"),
    # path('dashboard_student/',QuizListView.as_view(),name ="main-view"),
    path("dashboard_student/<pk>/", quiz_View, name='quiz-view'),
     path('dashboard_student/<pk>/save/', save_quiz_view, name='save-view'),
    path("dashboard_student/<pk>/data/", quiz_data_view, name='quiz-data-view'),
    path("dashboard_student/<pk>/feedback/", feedback_view, name='feedback'),
    path("dashboard_student/<pk>/feedback/save", save_feedback_view, name='feedback_save'),

#student-view-in staff dashboard 
    path("Login_staff/", log_in_staff, name='login_staff'),
    path('logout_staff/', log_out_staff, name='logout_staff'),
    path('dashboard_staff/',staff_home,name ="home_view"),
    path('dashboard_staff/studentList',studentList,name ="student_List"),
     path('dashboard_staff/studentList/add',student_add,name ="student_add"),
     path('dashboard_staff/studentList/edit',student_edit,name ="student_edit"),
    path('dashboard_staff/studentList/edit/update/<id>',student_update,name ="student_update"),
    path('dashboard_staff/studentList/edit/delete/<id>',student_delete,name ="student_delete"),

#Result view in staff dashboard
   path('dashboard_staff/ResultList',ResultList,name ="Result_List"),
   path('dashboard_staff/feedbackList',feedbackList,name ="feedback_List"),
# Quiz list in staff
    path('dashboard_staff/quizList',quizListStaff,name ="quiz_List_staff"),
    path('dashboard_staff/quizList/add',quiz_add,name ="quiz_add"),
    path('dashboard_staff/quizList/edit',quiz_edit,name ="quiz_edit"),
    path('dashboard_staff/quizList/edit/update/<id>',quiz_update,name ="quiz_update"),
    path('dashboard_staff/quizList/edit/delete/<id>',quiz_delete,name ="quiz_delete"),


    #Questions 
    path('dashboard_staff/questionList',questionListStaff,name ="question_List_staff"),
    # path('dashboard_staff/questionList/add',question_add,name ="question_add"),
    path('dashboard_staff/questionList/edit',question_edit,name ="question_edit"),
    path('dashboard_staff/questionList/edit/update/<id>',question_update,name ="question_update"),
    path('dashboard_staff/questionList/edit/delete/<id>',question_delete,name ="question_delete"),

    # testing
    # path('products/', ProductList.as_view(), name='list_products'),
    path('create/', QuestionCreate.as_view(), name='create_question'),
    path('update/<int:pk>/', QuestionUpdate.as_view(), name='update_question'),
    path('delete-image/<int:pk>/', delete_answer, name='delete_answer'),
    
   
]
