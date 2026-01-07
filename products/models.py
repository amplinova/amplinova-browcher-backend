from django.db import models
from .utils import get_initials, generate_logo_from_text

class Product(models.Model):
    STATUS_CHOICES = (
        ("live", "Live"),
        ("ongoing", "Ongoing"),
    )

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)  # for /ourProducts/restaurant
    logo = models.ImageField(upload_to="products/logos/",blank=True,null=True)

    def save(self, *args, **kwargs):
        if not self.logo:
            initials = get_initials(self.title)
            self.logo = generate_logo_from_text(initials)

        super().save(*args, **kwargs)



    #details
    duration = models.CharField(max_length=100, blank=True)
    category = models.CharField(max_length=100,blank=True)
    domain = models.CharField(max_length=100, blank=True)

    website_url = models.URLField(blank=True)
    website_label = models.CharField(
        max_length=50,
        default="Visit Website"
    )
     # DESCRIPTION
    description_heading = models.CharField(
        max_length=200, default="Project Description")
    
   # MEDIA
    video = models.FileField(
        upload_to="clients/videos/",
        blank=True,
        null=True
    )

    #meta
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="live"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class ProductDescriptionPoint(models.Model):
    product = models.ForeignKey(
        Product,
        related_name="description_points",
        on_delete=models.CASCADE
    )
    point = models.CharField(max_length=300)

    def __str__(self):
        return self.point


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        related_name="images",
        on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to="products/images/")

    def __str__(self):
        return f"Image for {self.product.title}"
