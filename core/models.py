from django.db import models
from atlas_app.models import AtlasBaseModel

# Create your models here.
class ProjectStatus(AtlasBaseModel):
    project_name = models.CharField(max_length=200)
    status = models.CharField(max_length=100)

    focus = models.CharField(max_length=200, help_text="The primary area of focus")
    activity = models.CharField(max_length=200)
    
    # Larger text areas for detailed strings
    pai_actions_overnight = models.TextField(verbose_name="PAI Actions Overnight")
    your_focus_today = models.TextField(verbose_name="Your Focus Today")

    query_count = models.IntegerField(default=0)

    class Meta:
        # This fixes the display in the sidebar
        verbose_name_plural = "Project Statuses"

    def __str__(self):
            return f"{self.project_name} - {self.focus}"

class Checklist(AtlasBaseModel):
    task_name = models.CharField(max_length=255)
    
    # New Status Checkboxes
    to_do = models.BooleanField(default=False)
    doing = models.BooleanField(default=False)
    is_done = models.BooleanField(default=False)

    # RELATION: This links the task to your ProjectStatus table
    # Now, one "ProjectStatus" can have many "Checklist" items
    project_status = models.ForeignKey(
        ProjectStatus, 
        on_delete=models.CASCADE, 
        related_name='checklists',
        null=True, 
        blank=True
    )
    
    # Relations
    portfolio_capsule = models.ForeignKey(
        'portfolio.PortfolioCapsule', 
        on_delete=models.CASCADE, 
        related_name='checklists', 
        null=True, 
        blank=True
    )
    curriculum_capsule = models.ForeignKey(
        'curriculum.CurriculumCapsule', 
        on_delete=models.CASCADE, 
        related_name='checklists', 
        null=True, 
        blank=True
    )
    
    def __str__(self):
        return self.task_name
