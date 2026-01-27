from django.contrib import admin
# You must add this line to link your model:
from .models import ProjectStatus, CurriculumCapsule, CurriculumCourse, CurriculumModule, CurriculumLesson, PortfolioCapsule, PortfolioMockup, Checklist

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

@admin.register(PortfolioCapsule)
class PortfolioCapsuleAdmin(admin.ModelAdmin):
    # These names must match the fields inside your PortfolioCapsule model
    list_display = ('title', 'status', 'last_updated')
    search_fields = ('title',)
    list_filter = ('status',)
    # Use this to easily move mockups between 'Available' and 'Selected'
    filter_horizontal = ('mockups',)
    
    # This organizes the "Edit" page
    fields = ('title', 'status', 'repo_url', 'mockups')
    inlines = [ChecklistInline]

@admin.register(PortfolioMockup)
class PortfolioMockupAdmin(admin.ModelAdmin):
    # display_capsules is a custom method defined below
    list_display = ('title', 'status', 'display_capsules', 'last_updated')
    search_fields = ('title', 'description')
    list_filter = ('status', 'portfolio_capsules') # Uses the related_name we set earlier

    def display_capsules(self, obj):
        # This joins all capsule titles into one string for the list view
        return ", ".join([capsule.title for capsule in obj.portfolio_capsules.all()])
    
    # Sets the column header in the Admin
    display_capsules.short_description = 'Capsules'

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

# Detailed view for your Curriculum Capsules
@admin.register(CurriculumCapsule)
class CurriculumCapsuleAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'last_updated')
    search_fields = ('title',)
    list_filter = ('status',)
    inlines = [ChecklistInline]

# 5. Optional: Keep the main Checklist table accessible on its own
@admin.register(Checklist)
class ChecklistAdmin(admin.ModelAdmin):
    list_display = ('task_name', 'is_done', 'last_updated')
    list_filter = ('is_done', 'to_do', 'doing')