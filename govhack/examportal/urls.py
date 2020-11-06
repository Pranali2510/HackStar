from django.urls import path
from .import  views

urlpatterns=[
     path('', views.home, name='home'),
     path('login/dash/', views.dash, name='dash'),
     path('candidate_register/',views.candidate_register.as_view(), name='candidate_register'),
     path('institute_register/',views.institute_register.as_view(), name='institute_register'),
     path('login/',views.login_request, name='login'),
     path('logout/',views.logout_view, name='logout'),
     path('searchbar/', views.searchbar, name='searchbar'),
     path('search/', views.search, name='search'),
     path('filter/', views.filter, name='filter'),
     path('home2/', views.home2, name='home2'),
     path('home3/', views.home3, name='home3'),
     path('result/', views.result, name='result'),

]