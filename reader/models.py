from django.db import models

# Create your models here.
class reader(models.Model):
    class Meta:
        app_label = "reader"
        db_table = 'reader'
    id = models.CharField(max_length=20,primary_key=True)
    name = models.CharField(max_length=100)
    passwd = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    status = models.CharField(max_length=20)
    createTime = models.DateTimeField(max_length=50)
