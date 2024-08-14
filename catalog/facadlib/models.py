from django.db import models

# Create your models here.
class Advertisement(models.Model):
    main_id = models.IntegerField()
    ad_id = models.IntegerField()
    text = models.TextField()
    link = models.URLField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.main_id} - {self.ad_id}'
    
class PagesToMonitor(models.Model):
    url = models.URLField()
    date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.url
    