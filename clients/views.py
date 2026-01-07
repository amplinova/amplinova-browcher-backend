from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import Client, ClientImage, ClientDescriptionPoint
from .serializers import (
    ClientListSerializer,
    ClientDetailSerializer,
    ClientCreateSerializer
)


class ClientListAPIView(APIView):
    http_method_names = ["get", "post"]

    def get(self, request):
        clients = Client.objects.all().order_by("-id")
        serializer = ClientListSerializer(clients, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = {
            "title": request.data.get("title"),
            "duration": request.data.get("duration", ""),
            "category": request.data.get("category", ""),
            "domain": request.data.get("domain", ""),
            "website_url": request.data.get("link", ""),
            "status": request.data.get("status", "live"),
        }

        if "logo" in request.FILES:
            data["logo"] = request.FILES["logo"]

        if "video" in request.FILES:
            data["video"] = request.FILES["video"]

        serializer = ClientCreateSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        client = serializer.save()

        # description bullets
        for point in request.data.getlist("description"):
            ClientDescriptionPoint.objects.create(
                client=client,
                point=point
            )

        # images
        for img in request.FILES.getlist("images"):
            ClientImage.objects.create(
                client=client,
                image=img
            )

        return Response(
            ClientDetailSerializer(client).data,
            status=status.HTTP_201_CREATED
        )


class ClientDetailAPIView(APIView):
    def get(self, request, slug):
        client = get_object_or_404(Client, slug=slug)
        serializer = ClientDetailSerializer(client)
        return Response(serializer.data)
