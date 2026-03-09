from django.db import models

# Create your models here.
class predicted_results(models.Model):
    id = models.IntegerField(primary_key=True)
    ques_ans = models.TextField()
    marks = models.CharField(max_length=100)
    final_result = models.TextField()

    def __str__(self) -> str:
        return super().__str__()
    
class questions_random(models.Model):
    id = models.IntegerField(primary_key=True)
    question = models.TextField()
    marks = models.CharField(max_length=100)

    def __str__(self) -> str:
        return super().__str__()