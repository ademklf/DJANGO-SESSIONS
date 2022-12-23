from django.db import models

# Create your models here.
from django.db import models

class Student(models.Model):
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=40)
    number = models.PositiveSmallIntegerField(blank=True, null=True)


    def __str__(self):
        return f'{self.number} - {self.first_name} {self.last_name}'
    
    class Meta:
       ordering = ('-number',) 
       verbose_name = 'öğrenci'
       verbose_name_plural = 'öğrenciler'
       