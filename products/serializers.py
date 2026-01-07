from rest_framework import serializers
from .models import (
    Product, 
    ProductImage,
    ProductDescriptionPoint
)


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["image"]


class ProductDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductDescriptionPoint
        fields = ["point"]


class ProductDetailSerializer(serializers.ModelSerializer):
    details = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    media = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "slug",
            "title",
            "logo",
            "details",
            "description",
            "media",
            "status",
        ]

    def get_details(self, obj):
        return {
            "duration": obj.duration or "",
            "category": obj.category or "",
            "domain": obj.domain or "",
            "website": {
                "url": obj.website_url or "",
                "label": obj.website_label or "Visit Website",
            }
        }

    def get_description(self, obj):
        return {
            "heading": obj.description_heading or "Project Description",
            "points": [p.point for p in obj.description_points.all()]
        }

    def get_media(self, obj):
        return {
            "images": [img.image.url for img in obj.images.all()],
            "video": {
                "src": obj.video.url if obj.video else "",
                "type": "video/mp4",
            }
        }
    

class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "title",
            "logo",
            "category",
            "domain",
            "status",
            "slug",
        ]



class ProductCreateSerializer(serializers.ModelSerializer):
    website_url = serializers.CharField(
        required=False,
        allow_blank=True
    )
    logo = serializers.ImageField(
        required=False,
        allow_null=True
    )


    class Meta:
        model = Product
        fields = [
            "title",
            "logo",
            "duration",
            "category",
            "domain",
            "website_url",
            "website_label",
            "video",
            "status",
        ]

    def create(self, validated_data):
        from django.utils.text import slugify

        validated_data["slug"] = slugify(validated_data["title"])

        # normalize empty website_url
        if not validated_data.get("website_url"):
            validated_data["website_url"] = ""

        return super().create(validated_data)
