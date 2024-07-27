from django.db import models
from django.contrib.auth.models import AbstractUser, Group

# Define choices for different roles
class Role(models.TextChoices):
    ADMIN = 'admin', 'Admin'
    MANAGER = 'manager', 'Manager'
    TEAM_MEMBER = 'team_member', 'Team Member'

# Extend Django's AbstractUser to include additional fields
class UserProfile(AbstractUser):
    # Additional fields specific to your application
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.TEAM_MEMBER)

    # Override the __str__ method to display user's full name
    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    # Override the save method to automatically add user to a group based on their role
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Call the save method of the parent class
        # Get or create a group based on the user's role
        group, created = Group.objects.get_or_create(name=self.role)
        self.groups.add(group)  # Add the user to the group