from django.db import models


class Client(models.Model):
    name = models.CharField(max_length=200)
    status = models.CharField(
        max_length=20,
        choices=(
            ("live", "Live"),
            ("ongoing", "Ongoing"),
        ),
        default="live"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200)
    status = models.CharField(
        max_length=20,
        choices=(
            ("live", "Live"),
            ("ongoing", "Ongoing"),
        ),
        default="live"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class TeamMember(models.Model):
    DEPARTMENT_CHOICES = (
        ("it", "IT"),
        ("digital_marketing", "Digital Marketing"),
        ("sales", "Sales"),
    )

    name = models.CharField(max_length=200)
    department = models.CharField(
        max_length=50,
        choices=DEPARTMENT_CHOICES
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.department})"
