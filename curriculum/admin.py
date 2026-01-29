#curriculum/admin.py
from django.contrib import admin
# 1. Import the Inline class from your core admin file
from core.admin import Checklist
# Register your models here.
from .models import CurriculumCapsule, CurriculumCourse, CurriculumModule, CurriculumLesson


# Lesson Inline (To show inside Module)
class CurriculumLessonInline(admin.TabularInline):
    model = CurriculumLesson
    extra = 1  # Shows one empty row by default

# 2. Module Inline (To show inside Course)
class CurriculumModuleInline(admin.TabularInline):
    model = CurriculumModule
    extra = 1

# 3. Registering the Models
@admin.register(CurriculumCourse)
class CurriculumCourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'last_updated')
    inlines = [CurriculumModuleInline]

@admin.register(CurriculumModule)
class CurriculumModuleAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order')
    list_filter = ('course',)
    inlines = [CurriculumLessonInline]

@admin.register(CurriculumLesson)
class CurriculumLessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'module', 'order', 'duration', 'is_completed')
    list_filter = ('module__course', 'is_completed')
# Define the inline right here in this file
class ChecklistInline(admin.TabularInline):
    model = Checklist
    extra = 1
    fields = ('task_name', 'to_do', 'doing', 'is_done')
# Detailed view for your Curriculum Capsules
@admin.register(CurriculumCapsule)
class CurriculumCapsuleAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'last_updated')
    search_fields = ('title',)
    list_filter = ('status',)
    inlines = [ChecklistInline]


