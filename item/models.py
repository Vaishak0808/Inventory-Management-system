from django.db import models

# Create your models here.
class item(models.Model):
    id = models.BigAutoField(primary_key=True)
    vchr_name = models.CharField(max_length=100)
    txt_description = models.TextField()
    int_status = models.IntegerField(blank=True, null=True,default = 1)
    
    class Meta:
        db_table = "item"