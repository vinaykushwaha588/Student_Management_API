from django.urls import path
from api import views

urlpatterns = [
    path('student-class', views.CreateClassView.as_view()),
    path('register-student', views.RegisterStudentView.as_view()),
    path('login-student', views.StudentLoginView.as_view()),
    path('update-student', views.GetUpdateStudentView.as_view()),
    path('perm-student/<int:pk>', views.StudentPermissionView.as_view()),
]
