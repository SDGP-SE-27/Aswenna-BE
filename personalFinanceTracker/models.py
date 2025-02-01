# from django.db import models
# from django.conf import settings


# class Expense(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     expense_type = models.CharField(max_length=255)
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     description = models.TextField(blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     date = models.DateField()


#     def __str__(self):
#         return f"{self.expense_type} - Rs.{self.amount}"

# class Income(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     income_type = models.CharField(max_length=255)
#     amount = models.DecimalField(max_digits=10 , decimal_places=2)
#     description = models.TextField(blank=True , null= True)
#     created_at = models.DateTimeField(auto_now_add=True) 
#     date = models.DateField()

#     def __str__(self):
#         return f"{self.income_type} - Rs.{self.amount}"


from django.db import models
from django.conf import settings

class Expense(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    expense_type = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    date = models.DateField()

    def __str__(self):
        return f"{self.expense_type} - Rs.{self.amount}"

class Income(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    income_type = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    date = models.DateField()

    def __str__(self):
        return f"{self.income_type} - Rs.{self.amount}"
