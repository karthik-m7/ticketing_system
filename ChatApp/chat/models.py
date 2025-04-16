from django.db import models
from django.utils import timezone

class User(models.Model):
    """Represents a visitor submitting a ticket (auto-created from ticket form)."""
    name = models.CharField(max_length=100)
    email = models.EmailField()
    number = models.CharField(max_length=15)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

class Staff(models.Model):
    """Represents staff members handling tickets."""
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    number = models.CharField(max_length=15)
    created_at = models.DateTimeField(default=timezone.now)
    designation = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Ticket(models.Model):
    """Represents a support ticket submitted by a visitor."""
    STATUS_CHOICES = [
        ('OPEN', 'Open'),
        ('IN_PROGRESS', 'In Progress'),
        ('RESOLVED', 'Resolved'),
        ('CLOSED', 'Closed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tickets')
    staff = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tickets')
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='ticket_images/', null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='OPEN')

    def __str__(self):
        return f"Ticket #{self.id} - {self.title}"

class Message(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='messages')
    sender_name = models.CharField(max_length=100)
    sender_type = models.CharField(max_length=10, choices=[('user', 'User'), ('staff', 'Staff')])  # <-- Add this
    message = models.TextField()
    image = models.ImageField(upload_to='message_images/', null=True, blank=True)
    datetime = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Message #{self.id} - Ticket #{self.ticket.id}"

