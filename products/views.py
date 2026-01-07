from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.utils.text import slugify

from .models import Product, ProductImage, ProductDescriptionPoint
from .serializers import (
    ProductListSerializer,
    ProductDetailSerializer,
    ProductCreateSerializer
)
class ProductListAPIView(APIView):
    http_method_names = ["get", "post"]
    def get(self, request):
        products = Product.objects.all().order_by("-id")
        serializer = ProductListSerializer(products, many=True)
        return Response(serializer.data)


    def post(self, request):
        print("POST HIT")

        # ✅ build clean dict (NO copy, NO deepcopy)
        data = {
            "title": request.data.get("title"),
            "duration": request.data.get("duration", ""),
            "category": request.data.get("category", ""),
            "domain": request.data.get("domain", ""),
            "website_url": request.data.get("link", ""),  # map frontend field
            "status": request.data.get("status", "live"),
        }

        # ✅ files handled separately
        if "logo" in request.FILES:
            data["logo"] = request.FILES["logo"]

        if "video" in request.FILES:
            data["video"] = request.FILES["video"]

        serializer = ProductCreateSerializer(data=data)

        if not serializer.is_valid():
            print("❌ SERIALIZER ERRORS:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        product = serializer.save()

        # ✅ description bullets
        for point in request.data.getlist("description"):
            if point.strip():
                ProductDescriptionPoint.objects.create(
                    product=product,
                    point=point
            )

        # ✅ multiple images
        for img in request.FILES.getlist("images"):
            ProductImage.objects.create(
                product=product,
                image=img
            )

        return Response(
            ProductDetailSerializer(product).data,
            status=status.HTTP_201_CREATED
        )

class ProductDetailAPIView(APIView):
    def get(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        serializer = ProductDetailSerializer(product)
        return Response(serializer.data)
