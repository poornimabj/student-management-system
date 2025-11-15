from django import forms
from .models import Student, Grade, Attendance, Teacher
from django.contrib.auth.forms import AuthenticationForm

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'roll_no', 'class_name', 'dob']

class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['name', 'employee_id', 'subject', 'email', 'phone']

class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['student', 'subject', 'marks', 'grade']

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['student', 'date', 'subject', 'is_present']

# optional custom login form (uses default AuthenticationForm is fine)
class LoginForm(AuthenticationForm):
    pass
