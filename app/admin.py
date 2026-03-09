from django.contrib import admin
from .models import predicted_results, questions_random
# Register your models here.

admin.site.register(predicted_results)
admin.site.register(questions_random)