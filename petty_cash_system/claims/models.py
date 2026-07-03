from django.db import models
from django.contrib.auth.models import AbstractUser

# 1. Custom User Model - യൂസർമാരെയും അവരുടെ റോളുകളെയും തിരിക്കാൻ
class User(AbstractUser):
    ROLE_CHOICES = (
        ('EMPLOYEE', 'Employee'),
        ('MANAGER', 'Manager'),
        ('FINANCE', 'Finance'),
        ('ADMIN', 'Admin'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='EMPLOYEE')

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

# 2. Petty Cash Claim Model
class Claim(models.Model):
    CATEGORY_CHOICES = (
        ('Meals', 'Meals'),
        ('Food', 'Food'),
        ('Travel', 'Travel'),
        ('Fuel', 'Fuel'),
        ('Office Expense', 'Office Expense'),
        ('Stationery', 'Stationery'),
        ('Other', 'Other'),
    )

    STATUS_CHOICES = (
        ('Pending Manager Approval', 'Pending Manager Approval'),
        ('Manager Approved', 'Manager Approved'),
        ('Manager Rejected', 'Manager Rejected'),
        ('Pending Finance Approval', 'Pending Finance Approval'),
        ('Finance Approved', 'Finance Approved'),
        ('Finance Rejected', 'Finance Rejected'),
        ('Paid', 'Paid'),
    )

    employee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='claims')
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    receipt = models.ImageField(upload_to='receipts/')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending Manager Approval')
    submitted_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.employee.username} ({self.amount})"

# 3. Approval History Model
class ApprovalHistory(models.Model):
    claim = models.ForeignKey(Claim, on_delete=models.CASCADE, related_name='history')
    approver = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=50)
    action = models.CharField(max_length=50) # Approved, Rejected, Paid
    remarks = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.claim.title} - {self.action} by {self.approver.username}"