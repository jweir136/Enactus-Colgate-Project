from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class CompletedModules(models.Model):
    username = models.CharField(max_length=1000)
    points = models.IntegerField(default=0)
    module_id = models.IntegerField(default=-1)

    def __str__(self):
        return "{} {} {}".format(self.module_id, self.username, self.points)

class LearningModules(models.Model):
    module_id = models.AutoField(primary_key=True)
    module_title = models.CharField(max_length=500)
    module_summary = models.CharField(max_length=1000)
    module_text = models.CharField(max_length=1000000)
    module_action_link = models.URLField(max_length=1000)
    module_points = models.IntegerField(default=0)
    
    def __str__(self):
        return "<LearningModule {}>".format(self.module_title)