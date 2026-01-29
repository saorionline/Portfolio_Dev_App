#core/admin.py

from django.contrib import admin

# Register your models here.
from .models import ProjectStatus, Checklist

# 5. Optional: Keep the main Checklist table accessible on its own
@admin.register(Checklist)
class ChecklistAdmin(admin.ModelAdmin):
    list_display = ('task_name', 'is_done', 'last_updated')
    list_filter = ('is_done', 'to_do', 'doing')

# 1. This allows Checklists to appear inside other pages
class ChecklistInline(admin.TabularInline):
    model = Checklist
    extra = 1  # This provides 1 empty row to quickly add a new task
    fields = ('task_name', 'to_do', 'doing', 'is_done')

# Simple registration for the Status list (Draft, Completed, etc.)
@admin.register(ProjectStatus)
class ProjectStatusAdmin(admin.ModelAdmin):
    list_display = ('project_name', 'focus', 'activity', 'status', 'last_updated')
    # Allows you to search through these specific fields
    search_fields = (
        'project_name', 
        'focus', 
        'activity', 
        'projects__name', 
        'capsules__title',
        'checklists__task_name')
    inlines = [ChecklistInline] # <--- This adds the Checklist at the bottom
    
    # Optional: adds a filter sidebar on the right
    list_filter = ('status', 'focus')
    # This organizes the "Edit" page
    # Putting ('focus', 'activity') in a tuple displays them on the same line!
    fields = ('project_name', ('focus', 'activity'), 'status', 'pai_actions_overnight', 'your_focus_today')

