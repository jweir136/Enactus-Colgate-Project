from django.contrib import admin
from .models import LearningModules, CompletedModules

# Register your models here.
admin.site.register(LearningModules)
admin.site.register(CompletedModules)