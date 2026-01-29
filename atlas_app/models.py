from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
class ProjectStatus(models.Model):
    # The first argument is the "verbose_name" (the label shown in Admin)
    project_name = models.CharField(_("project name"), max_length=200)
    status = models.CharField(_("status"), max_length=100)

    focus = models.CharField(_("focus"), max_length=200, help_text="The primary area of focus")
    activity = models.CharField(_("activity"), max_length=200)
    
    # Larger text areas for detailed strings
    pai_actions_overnight = models.TextField(verbose_name=_("PAI Actions Overnight"))
    your_focus_today = models.TextField(verbose_name=_("Your Focus Today"))

    last_updated = models.DateTimeField(auto_now=True, null=True, blank=True)
    query_count = models.IntegerField(_("query count"), default=0)

    class Meta:
        # This fixes the display in the sidebar
        verbose_name = _("Project Status")
        verbose_name_plural = _("Project Statuses")

    def __str__(self):
            return f"{self.project_name} - {self.focus}"
    
class CurriculumCapsule(models.Model):
    title = models.CharField(_("title"), max_length=200)
    # This links to the table above
    status = models.ForeignKey(
        'ProjectStatus',
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='curriculum_capsules',
        verbose_name=_("status")
    )
    last_updated = models.DateTimeField(_("last updated"), auto_now=True, null=True, blank=True)

    class Meta:
        verbose_name = _("Curriculum Capsule")
        verbose_name_plural =_("Curriculum Capsules")

    def __str__(self):
        return self.title
    
class CurriculumCourse(models.Model):
    title = models.CharField(_("title"), max_length=200) # e.g., "FastAPI"
    capsule = models.ForeignKey('CurriculumCapsule', 
                               on_delete=models.SET_NULL, 
                               null=True, 
                               related_name='courses',
                               verbose_name=_("capsule")
    )
    status = models.ForeignKey(
        'ProjectStatus', 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='detailed_courses',
        verbose_name=_("status")
        )
    last_updated = models.DateTimeField(_("last updated"), auto_now=True, null=True, blank=True)

    class Meta:
        verbose_name = _("Curriculum Course")
        verbose_name_plural = _("Curriculum Courses")

    def __str__(self):
        return self.title

class CurriculumModule(models.Model):
    course = models.ForeignKey(
        'CurriculumCourse', 
        on_delete=models.CASCADE, 
        related_name='modules',
        verbose_name=_("course")
        )
    title = models.CharField(_("title"), max_length=200) # e.g., "Introduction to FastAPI"
    order = models.IntegerField(_("order"), default=1)

    class Meta:
            verbose_name = _("Curriculum Module")
            verbose_name_plural = _("Curriculum Modules")

    def __str__(self):
        return f"{self.course.title} - {self.title}"

class CurriculumLesson(models.Model):
    module = models.ForeignKey(
        'CurriculumModule', 
        on_delete=models.CASCADE,
        related_name='lessons',
        verbose_name=_("module")
        )
    title = models.CharField(_("title"), max_length=200)
    order = models.IntegerField(_("order"))
    duration = models.CharField(_("duration"), max_length=10) # Storing as "MM:SS"
    is_completed = models.BooleanField(_("is completed"), default=False)

    class Meta:
        verbose_name = _("Curriculum Lesson")
        verbose_name_plural = _("Curriculum Lessons")

    def __str__(self):
        return f"{self.order}. {self.title}"

class PortfolioMockup(models.Model):
    title = models.CharField(_("title"), max_length=200)
    description = models.TextField(_("description"), blank=True) 
    status = models.ForeignKey(
        'ProjectStatus', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='portfolio_mockups',
        verbose_name=_("status")
    )
    # To store the text you provided
    last_updated = models.DateTimeField(_("last updated"), auto_now=True, null=True, blank=True)

    class Meta:
        verbose_name = _("Portfolio Mockup")
        verbose_name_plural = _("Portfolio Mockups")

    def __str__(self):
        return self.title

class PortfolioCapsule(models.Model):
    title = models.CharField(_("title"), max_length=200)
    # Changed to ManyToManyField
    mockups = models.ManyToManyField(
        'PortfolioMockup',
        related_name='portfolio_capsules',
        blank=True,
        verbose_name=_("mockups")
    )    # This also links to the table above
    status = models.ForeignKey(
        ProjectStatus, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='portfolio_capsule_status'
    )
    last_updated = models.DateTimeField(_("last updated"), auto_now=True, null=True, blank=True)
    repo_url = models.URLField(_("repository URL"), blank=True)

    class Meta:
        verbose_name = _("Portfolio Capsule")
        verbose_name_plural = _("Portfolio Capsules")

    def __str__(self):
        return self.title

class Checklist(models.Model):
    task_name = models.CharField(_("task name"),max_length=255)
    
    # New Status Checkboxes
    to_do = models.BooleanField(_("to do"), default=False)
    doing = models.BooleanField(_("doing"), default=False)
    is_done = models.BooleanField(_("is done"), default=False)

    # RELATION: This links the task to your ProjectStatus table
    # Now, one "ProjectStatus" can have many "Checklist" items
    project_status = models.ForeignKey(
        'ProjectStatus', 
        on_delete=models.CASCADE, 
        related_name='checklists',
        null=True, 
        blank=True,
        verbose_name=_("project status")
    )
    
    # Relations
    portfolio_capsule = models.ForeignKey(
        'PortfolioCapsule', 
        on_delete=models.CASCADE, 
        related_name='checklists', 
        null=True, 
        blank=True,
        verbose_name=_("portfolio capsule")
    )
    curriculum_capsule = models.ForeignKey(
        'CurriculumCapsule', 
        on_delete=models.CASCADE, 
        related_name='checklists', 
        null=True, 
        blank=True,
        verbose_name=_("curriculum capsule")
    )
    
    last_updated = models.DateTimeField(_("last updated"), auto_now=True)

    class Meta:
        verbose_name = _("Checklist")
        verbose_name_plural = _("Checklists")

    def __str__(self):
        return self.task_name
