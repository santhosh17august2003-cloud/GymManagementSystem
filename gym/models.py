from django.db import models
from django.contrib.auth.models import User


class fee(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    Fee = models.IntegerField(default=0)  
    Actualfee = models.IntegerField(default=0) 
    Pendingfee = models.IntegerField(default=0) 
    Datetime = models.CharField(max_length=100, default="")

    def __str__(self):
        return f"Fee for {self.user.username if self.user else 'N/A'} on {self.Datetime}"
    
class Attendance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    month = models.CharField(max_length=100, default="")
    attendance_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=[('Present', 'Present'), ('Absent', 'Absent')], default="Present")

    def __str__(self):
        return f"{self.user.username} - {self.attendance_date} - {self.status}"
class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)  
    def __str__(self):
        return self.name



    
        