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

    class Meta:
        # This fixes the display in the sidebar
        verbose_name_plural = "Project Statuses"

    def __str__(self):
            return f"{self.project_name} - {self.focus}"
    
class CurriculumCapsule(models.Model):
    title = models.CharField(max_length=200)
    # This links to the table above
    status = models.ForeignKey(ProjectStatus, on_delete=models.SET_NULL, null=True, related_name='capsules')
    last_updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Curriculum Capsules"

    def __str__(self):
        return self.title
    
class CurriculumCourse(models.Model):
    title = models.CharField(max_length=200) # e.g., "FastAPI"
    capsule = models.ForeignKey(CurriculumCapsule, 
                               on_delete=models.SET_NULL, 
                               null=True, 
                               related_name='courses'
    )
    status = models.ForeignKey(ProjectStatus, on_delete=models.SET_NULL, null=True, related_name='detailed_courses')
    last_updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Curriculum Courses"

    def __str__(self):
        return self.title

class CurriculumModule(models.Model):
    course = models.ForeignKey(CurriculumCourse, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField(max_length=200) # e.g., "Introduction to FastAPI"
    order = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.course.title} - {self.title}"

class CurriculumLesson(models.Model):
    module = models.ForeignKey(CurriculumModule, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    order = models.IntegerField()
    duration = models.CharField(max_length=10) # Storing as "MM:SS"
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.order}. {self.title}"


class PortfolioProject(models.Model):
    name = models.CharField(max_length=200)
    # This also links to the table above
    status = models.ForeignKey(ProjectStatus, on_delete=models.SET_NULL, null=True, related_name='projects')
    last_updated = models.DateTimeField(auto_now=True, null=True, blank=True)
    repo_url = models.URLField(blank=True)

class Checklist(models.Model):
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
    portfolio_project = models.ForeignKey(
        PortfolioProject, 
        on_delete=models.CASCADE, 
        related_name='checklists', 
        null=True, 
        blank=True
    )
    curriculum_capsule = models.ForeignKey(
        CurriculumCapsule, 
        on_delete=models.CASCADE, 
        related_name='checklists', 
        null=True, 
        blank=True
    )
    
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.task_name
