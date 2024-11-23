from django.contrib import admin
from authentication import models as api_models

# Register your models here.

admin.site.register(api_models.User)
