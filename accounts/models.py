from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import time

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    forget_password_token = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class StudentData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField()
    phone = models.CharField(max_length=20)
    school = models.CharField(max_length=100, default="-")
    major = models.CharField(max_length=100, default="-")
    graduation_year = models.CharField(max_length=4, default="2025")
    annual_income = models.CharField(max_length=100, default="less than 60,000 ₹")
    parent_name = models.CharField(max_length=100, default="-")
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    request_status = models.CharField(max_length=100, default='No Request')
    requested_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    transaction_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    transaction_category = models.CharField(max_length=100, choices=[
        ('Travelling', 'Travelling'),
        ('Study Material', 'Study Material'),
        ('Food', 'Food'),
        ('Miscellaneous', 'Miscellaneous'),
    ], default='Travelling')
    transaction_note = models.TextField(default="")
    transaction_history = models.JSONField(default=list)
    transaction_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.user.username

    def add_transaction(self, amount, category, note):
        transaction = {
            'amount': str(amount),
            'category': category,
            'note': note,
            'time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        }
        self.transaction_history.append(transaction)
        self.save()

    def get_transaction_history_with_time(self):
        for transaction in self.transaction_history:
            transaction['time'] = transaction['time']
            if transaction['category'] == 'Money Request':
                transaction['request_status'] = self.request_status
        return self.transaction_history

    def create_money_request(self, amount):
        if self.request_status == 'No Request':
            self.requested_amount = amount
            self.request_status = 'Pending'
            self.save()
            self.add_transaction(amount, 'Money Request', 'Money request generated')

    def get_transaction_history(self):
        return self.transaction_history
