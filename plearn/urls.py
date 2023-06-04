from django import urls
from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.redirectToPlearn),
    path('index/', views.redirectToPlearn, name='indexAlt'),
    path('index/<int:id>', views.plearn, name='index'),
    path('signin/', views.auth, name='signin'),
    path('signup/', views.register, name='signup'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout_user, name='logout'),
    path('create-section/', views.create_section, name='create_section'),
    path('edit-section/<int:id>', views.edit_section, name='edit_section'),
    path('discussions/<int:id>', views.discussions, name='discussions'),
    path('replies/<int:secId>', views.replies, name='replies'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
]