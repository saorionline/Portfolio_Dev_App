from django.contrib import admin
# You must add this line to link your model:
from .models import ProjectStatus

# Register your models here.
@admin.register(ProjectStatus)
class ProjectStatusAdmin(admin.ModelAdmin):
    list_display = ('project_name', 'focus', 'activity', 'status', 'last_updated')
    # Allows you to search through these specific fields
    search_fields = ('project_name', 'focus', 'activity')
    
    # Optional: adds a filter sidebar on the right
    list_filter = ('status', 'focus')
    # This organizes the "Edit" page
    # Putting ('focus', 'activity') in a tuple displays them on the same line!
    fields = ('project_name', ('focus', 'activity'), 'status', 'pai_actions_overnight', 'your_focus_today')