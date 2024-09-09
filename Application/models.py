from django.db import models
from django.contrib.auth.models import User

# Service model remains the same


class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price_per_word = models.DecimalField(max_digits=6, decimal_places=2)
    academic_levels = models.CharField(max_length=100)
    revisions = models.IntegerField(default=0)
    plagiarism_free = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

# Updated Order model to link with User


class Order(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    # Link to the User model
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    deadline = models.DateTimeField()
    word_count = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    plagiarism_free = models.BooleanField(default=True)
    revisions = models.IntegerField(default=0)
    order_status = models.CharField(max_length=50, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # New fields
    academic_level = models.CharField(max_length=100, blank=True, null=True)
    type_of_paper = models.CharField(max_length=100, blank=True, null=True)
    discipline = models.TextField(blank=True, null=True)
    instructions = models.TextField(blank=True, null=True)
    additional_materials = models.FileField(
        upload_to='additional_materials/', blank=True, null=True)
    deadline = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Order {self.id} - {self.user.username} ({self.service.name})"
