from django.db import models

# Create your models here.
class ProjectStatus(models.Model):
    project_name = models.CharField(max_length=200)
    status = models.CharField(max_length=100)

    focus = models.CharField(max_length=200, help_text="The primary area of focus")
    activity = models.CharField(max_length=200)
    
    # Larger text areas for detailed strings
    pai_actions_overnight = models.TextField(verbose_name="PAI Actions Overnight")
    your_focus_today = models.TextField(verbose_name="Your Focus Today")

    last_updated = models.DateTimeField(auto_now=True, null=True, blank=True)
    query_count = models.IntegerField(default=0)

    def __str__(self):
            return f"{self.project_name} - {self.focus}"
