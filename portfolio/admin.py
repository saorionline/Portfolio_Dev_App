
#portfolio/admin.py
from django.contrib import admin
# 1. Import the Inline class from your core admin file
from core.admin import ChecklistInline
# Register your models here.
from .models import PortfolioCapsule, PortfolioMockup


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
