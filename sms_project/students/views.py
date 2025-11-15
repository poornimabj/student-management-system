from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Student, Grade, Attendance, Teacher
from .forms import StudentForm, GradeForm, AttendanceForm, TeacherForm
from datetime import date
from django.db.models import Avg
from django.db import DatabaseError

def staff_required(user):
    return user.is_active and user.is_staff

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'students/login.html', {'error': 'Invalid credentials'})
    return render(request, 'students/login.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
@user_passes_test(staff_required)
def dashboard(request):
    total_students = Student.objects.count()
    todays = date.today()
    todays_attendance = Attendance.objects.filter(date=todays).count()
    avg_marks = Grade.objects.aggregate(avg=Avg('marks'))['avg'] or 0
    recent_students = Student.objects.order_by('-created_at')[:6]
    context = {
        'total_students': total_students,
        'todays_attendance': todays_attendance,
        'avg_marks': round(avg_marks, 2),
        'recent_students': recent_students
    }
    return render(request, 'students/dashboard.html', context)


@login_required
@user_passes_test(staff_required)
def student_list(request):
    qs = Student.objects.all().order_by('roll_no')
    q = request.GET.get('q')
    if q:
        qs = qs.filter(name__icontains=q) | qs.filter(roll_no__icontains=q)
    return render(request, 'students/student_list.html', {'students': qs})


@login_required
@user_passes_test(staff_required)
def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save()
            messages.success(request, "Student added.")
            return redirect('student_details', pk=str(student.pk))
    else:
        form = StudentForm()
    return render(request, 'students/add_student.html', {'form': form})


@login_required
@user_passes_test(staff_required)
def edit_student(request, pk):
    st = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=st)
        if form.is_valid():
            form.save()
            messages.success(request, "Updated.")
            return redirect('student_details', pk=str(st.pk))
    else:
        form = StudentForm(instance=st)
    return render(request, 'students/edit_student.html', {'form': form, 'student': st})


@login_required
@user_passes_test(staff_required)
def delete_student(request, pk):
    st = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        st.delete()
        messages.success(request, "Deleted student.")
        return redirect('student_list')
    return render(request, 'students/confirm_delete.html', {'student': st})


@login_required
@user_passes_test(staff_required)
def student_details(request, pk):
    st = get_object_or_404(Student, pk=pk)
    grades = st.grades.all().order_by('-date_recorded')
    attendance = st.attendance.all().order_by('-date')
    grade_form = GradeForm(initial={'student': st})
    attendance_form = AttendanceForm(initial={'student': st, 'date': date.today()})
    return render(request, 'students/student_details.html', {
        'student': st, 'grades': grades, 'attendance': attendance,
        'grade_form': grade_form, 'attendance_form': attendance_form
    })


@login_required
@user_passes_test(staff_required)
@login_required
@user_passes_test(staff_required)
def grade_list(request):
    grades = Grade.objects.all().order_by('-date_recorded')
    q = request.GET.get('q')
    if q:
        grades = grades.filter(student__name__icontains=q) | grades.filter(subject__icontains=q)
    return render(request, 'students/grade_list.html', {'grades': grades})


@login_required
@user_passes_test(staff_required)
def add_grade(request):
    if request.method == 'POST':
        form = GradeForm(request.POST)
        if form.is_valid():
            g = form.save(commit=False)
            g.recorded_by = request.user
            g.save()
            messages.success(request, "Grade recorded.")
            return redirect('student_details', pk=str(g.student.pk))
    else:
        form = GradeForm()
    return render(request, 'students/add_grade.html', {'form': form})


@login_required
@user_passes_test(staff_required)
def mark_attendance(request):
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.recorded_by = request.user
            try:
                obj.save()
                messages.success(request, "Attendance saved.")
                return redirect('student_details', pk=str(obj.student.pk))
            except:
                messages.error(request, "Attendance already exists for this student and date.")
    else:
        form = AttendanceForm()
    return render(request, 'students/mark_attendance.html', {'form': form})


@login_required
@user_passes_test(staff_required)
def attendance_report(request):
    # Subjects to report on (you can extend this list or make it dynamic)
    subjects = [
        'Maths',
        'Operating System',
        'Digital Design',
        'DSA',
        'Java',
        'Python'
    ]

    report = []
    error = None
    try:
        for subj in subjects:
            total = Attendance.objects.filter(subject__iexact=subj).count()
            present = Attendance.objects.filter(subject__iexact=subj, is_present=True).count()
            percent = round((present / total) * 100, 2) if total > 0 else 0
            report.append({'subject': subj, 'total': total, 'present': present, 'percentage': percent})
    except DatabaseError as e:
        # Likely cause: migrations not applied or Djongo translation issue.
        report = []
        error = str(e) or 'Database error (migrations may be unapplied).'

    context = {
        'report': report,
        'error': error,
    }
    return render(request, 'students/attendance_report.html', context)


@login_required
@user_passes_test(staff_required)
def settings_page(request):
    return render(request, 'settings.html')


@login_required
def change_password(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if not request.user.check_password(old_password):
            messages.error(request, 'Old password is incorrect.')
        elif new_password != confirm_password:
            messages.error(request, 'New passwords do not match.')
        elif len(new_password) < 8:
            messages.error(request, 'Password must be at least 8 characters long.')
        else:
            request.user.set_password(new_password)
            request.user.save()
            messages.success(request, 'Password changed successfully. Please login again.')
            return redirect('login')
    return render(request, 'change_password.html')


@login_required
@user_passes_test(staff_required)
def add_teacher(request):
    if request.method == 'POST':
        form = TeacherForm(request.POST)
        if form.is_valid():
            teacher = form.save()
            messages.success(request, "Teacher added successfully.")
            return redirect('teacher_details', pk=str(teacher.pk))
    else:
        form = TeacherForm()
    return render(request, 'students/add_teacher.html', {'form': form})


@login_required
@user_passes_test(staff_required)
def teacher_details(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    return render(request, 'students/teacher_details.html', {'teacher': teacher})


@login_required
@user_passes_test(staff_required)
def teacher_list(request):
    teachers = Teacher.objects.all().order_by('name')
    q = request.GET.get('q')
    if q:
        teachers = teachers.filter(name__icontains=q) | teachers.filter(employee_id__icontains=q) | teachers.filter(subject__icontains=q)
    return render(request, 'students/teacher_list.html', {'teachers': teachers})


@login_required
@user_passes_test(staff_required)
def edit_teacher(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    if request.method == 'POST':
        form = TeacherForm(request.POST, instance=teacher)
        if form.is_valid():
            form.save()
            messages.success(request, "Teacher updated successfully.")
            return redirect('teacher_details', pk=str(teacher.pk))
    else:
        form = TeacherForm(instance=teacher)
    return render(request, 'students/edit_teacher.html', {'form': form, 'teacher': teacher})


@login_required
@user_passes_test(staff_required)
def delete_teacher(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    if request.method == 'POST':
        teacher.delete()
        messages.success(request, "Teacher deleted successfully.")
        return redirect('teacher_list')
    return render(request, 'students/confirm_delete_teacher.html', {'teacher': teacher})
