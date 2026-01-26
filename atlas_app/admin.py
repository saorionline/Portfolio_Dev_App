from django.contrib import admin
# You must add this line to link your model:
from .models import ProjectStatus, CurriculumCapsule, PortfolioProject

# 1. Simple registration for the Status list (Draft, Completed, etc.)
@admin.register(ProjectStatus)

class ProjectStatusAdmin(admin.ModelAdmin):
    list_display = ('project_name', 'focus', 'activity', 'status', 'last_updated')
    # Allows you to search through these specific fields
    search_fields = (
        'project_name', 
        'focus', 
        'activity', 
        'projects__name', 
        'capsules__title')
    
    # Optional: adds a filter sidebar on the right
    list_filter = ('status', 'focus')
    # This organizes the "Edit" page
    # Putting ('focus', 'activity') in a tuple displays them on the same line!
    fields = ('project_name', ('focus', 'activity'), 'status', 'pai_actions_overnight', 'your_focus_today')

@admin.register(PortfolioProject)
class PortfolioProjectAdmin(admin.ModelAdmin):
    # These names must match the fields inside your PortfolioProject model
    list_display = ('name', 'status', 'last_updated')
    search_fields = ('name',)
    list_filter = ('status',)
    
    # This organizes the "Edit" page
    fields = ('name', 'status', 'repo_url')

# 3. Detailed view for your Curriculum Capsules
@admin.register(CurriculumCapsule)
class CurriculumCapsuleAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'last_updated')
    search_fields = ('title',)
    list_filter = ('status',)