from rest_framework import serializers
from django.utils.text import slugify
from .models import Client, ClientImage, ClientDescriptionPoint


class ClientImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientImage
        fields = ["image"]


class ClientDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientDescriptionPoint
        fields = ["point"]


class ClientListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ["title", "logo", "category","domain", "status", "slug"]


class ClientDetailSerializer(serializers.ModelSerializer):
    details = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    media = serializers.SerializerMethodField()

    class Meta:
        model = Client
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
            "duration": obj.duration,
            "category": obj.category,
            "domain": obj.domain,
            "website": {
                "url": obj.website_url,
                "label": obj.website_label,
            }
        }

    def get_description(self, obj):
        return {
            "heading": obj.description_heading,
            "points": [p.point for p in obj.description_points.all()]
        }

    def get_media(self, obj):
        return {
            "images": [img.image.url for img in obj.images.all()],
            "video": {
                "src": obj.video.url if obj.video else "",
                "type": "video/mp4"
            }
        }


class ClientCreateSerializer(serializers.ModelSerializer):
    logo = serializers.ImageField(required=False, allow_null=True)
    website_url = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = Client
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
        validated_data["slug"] = slugify(validated_data["title"])
        return super().create(validated_data)
