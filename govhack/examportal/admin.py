from django.contrib import admin

# Register your models here.
from . import models

admin.site.register(models.Institute)
admin.site.register(models.Candidate)
admin.site.register(models.User)



