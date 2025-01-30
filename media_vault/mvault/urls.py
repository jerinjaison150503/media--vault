from django.urls import path
from . import views

urlpatterns = [
    path('reg/', views.reg, name='reg'),  
    path('log/', views.log, name='log'),  
    path('home/', views.home, name='home'),  
    path('logout/', views.logout_view, name='logout_view'), 
    path('upload/', views.uploadfile, name='upload'),  
]
