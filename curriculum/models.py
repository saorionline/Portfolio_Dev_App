
# curriculum/models.py
from django.db import models
# This tells Python: "Go to the atlas_app folder, find models.py, and grab AtlasBaseModel"
from atlas_app.models import AtlasBaseModel

# Create your models here.
class CurriculumCapsule(AtlasBaseModel):
    # 'title' and 'last_updated' are already included!    # This links to the table above
    status = models.ForeignKey(
       'core.ProjectStatus',
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='curriculum_capsules'
    )

    class Meta:
        verbose_name_plural = "Curriculum Capsules"

    def __str__(self):
        return self.title
    
class CurriculumCourse(AtlasBaseModel):
    capsule = models.ForeignKey(CurriculumCapsule, 
                               on_delete=models.SET_NULL, 
                               null=True, 
                               related_name='courses'
    )
    status = models.ForeignKey(
        'core.ProjectStatus', 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='detailed_courses'
        )

    class Meta:
        verbose_name_plural = "Curriculum Courses"

    def __str__(self):
        return self.title

class CurriculumModule(AtlasBaseModel):
    course = models.ForeignKey(CurriculumCourse, on_delete=models.CASCADE, related_name='modules')
    order = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.course.title} - {self.title}"

class CurriculumLesson(AtlasBaseModel):
    module = models.ForeignKey(CurriculumModule, on_delete=models.CASCADE, related_name='lessons')
    order = models.IntegerField()
    duration = models.CharField(max_length=10) # Storing as "MM:SS"
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.order}. {self.title}"