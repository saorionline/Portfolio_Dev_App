from django.db import models
from atlas_app.models import AtlasBaseModel

# Create your models here.
class PortfolioMockup(AtlasBaseModel):
    description = models.TextField(blank=True) 
    status = models.ForeignKey(
        'core.ProjectStatus',  
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='portfolio_mockups'
    )

    def __str__(self):
        return self.title

class PortfolioCapsule(AtlasBaseModel):
    # Changed to ManyToManyField
    mockups = models.ManyToManyField(
        PortfolioMockup, 
        related_name='portfolio_capsules',
        blank=True
    )    # This also links to the table above
    status = models.ForeignKey(
        'core.ProjectStatus',  
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='portfolio_capsule_status'
    )
    repo_url = models.URLField(blank=True)

    def __str__(self):
        return self.title