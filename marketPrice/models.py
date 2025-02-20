from django.db import models

# Create your models here.

class DBTables(models.Model):
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField()
    retail_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    predicted_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    
    class Meta:
        abstract = True
        
        
class LongBeans(DBTables):
    class Meta:
        db_table = "long_beans"
        
class BitterGourd(DBTables):
    class Meta:
        db_table = "bitter_gourd"
        
        
class SnakeGourd(DBTables):
    class Meta:
        db_table = "snake_gourd"
        

class LadyFingerOkra(DBTables):
    class Meta:
        db_table = "ladys_finger_okra"
        
        
class Brinjals(DBTables):
    class Meta:
        db_table = "brinjals"
        
class Pineapple(DBTables):
    class Meta:
        db_table = "pineapple"
        
class Papaya(DBTables):
    class Meta:
        db_table = "papaya"