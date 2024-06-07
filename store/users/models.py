from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """Кастомний клас користувачiв"""

    USER_TYPE_CHOICES = (    # Валiднi користувачi
        ('CASHIER', 'Cashier'),
        ('CONSULTANT', 'Consultant'),
        ('ACCOUNTANT', 'Accountant')
    )

    user_type = models.TextField(choices=USER_TYPE_CHOICES, max_length=10)

    class Meta:
        verbose_name = 'Users'

    # Перевірка, чи є користувач касиром
    @property
    def is_cashier(self):
        return self.user_type == 'CASHIER'
    
    # Перевірка, чи є користувач консультантом
    @property
    def is_consultant(self):
        return self.user_type == 'CONSULTANT'

    # Перевірка, чи є користувач бухгалтером
    @property
    def is_accountant(self):
        return self.user_type == 'ACCOUNTANT'