from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('students/', views.student_list, name='student_list'),
    path('students/add/', views.add_student, name='add_student'),
    path('students/<str:pk>/', views.student_details, name='student_details'),
    path('students/<str:pk>/edit/', views.edit_student, name='edit_student'),
    path('students/<str:pk>/delete/', views.delete_student, name='delete_student'),

    path('teachers/', views.teacher_list, name='teacher_list'),
    path('teachers/add/', views.add_teacher, name='add_teacher'),
    path('teachers/<str:pk>/', views.teacher_details, name='teacher_details'),
    path('teachers/<str:pk>/edit/', views.edit_teacher, name='edit_teacher'),
    path('teachers/<str:pk>/delete/', views.delete_teacher, name='delete_teacher'),

    path('grades/', views.grade_list, name='grade_list'),
    path('grades/add/', views.add_grade, name='add_grade'),
    path('attendance/add/', views.mark_attendance, name='mark_attendance'),
    path('attendance/report/', views.attendance_report, name='attendance_report'),
    path('settings/', views.settings_page, name='settings_page'),
    path('change-password/', views.change_password, name='change_password'),
    path("add-student/", views.add_student, name="add_student"),
]
