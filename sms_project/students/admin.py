from django.contrib import admin
from .models import Student, Grade, Attendance, Teacher, ActivityLog

class GradeInline(admin.TabularInline):
    model = Grade
    extra = 0

class AttendanceInline(admin.TabularInline):
    model = Attendance
    extra = 0

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'roll_no', 'class_name', 'dob', 'created_at')
    search_fields = ('name', 'roll_no')
    list_filter = ('class_name', 'created_at')
    inlines = [GradeInline, AttendanceInline]

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('name', 'employee_id', 'subject', 'email', 'phone', 'created_at')
    search_fields = ('name', 'employee_id', 'subject')
    list_filter = ('subject', 'created_at')

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'marks', 'recorded_by', 'date_recorded')
    search_fields = ('student__name', 'subject')
    list_filter = ('subject', 'date_recorded')

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'date', 'is_present', 'recorded_by')
    search_fields = ('student__name', 'date')
    list_filter = ('date', 'is_present')

@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'model_name', 'object_name', 'timestamp')
    search_fields = ('user__username', 'model_name', 'object_name')
    list_filter = ('action', 'timestamp', 'model_name')
    readonly_fields = ('user', 'action', 'model_name', 'object_id', 'object_name', 'timestamp')

