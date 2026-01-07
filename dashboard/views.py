from rest_framework.views import APIView
from rest_framework.response import Response
from dashboard.models import Product
from dashboard.models import Client
from dashboard.models import TeamMember


class DashboardAPIView(APIView):
    def get(self, request):

        # 🟦 live client projects
        live_clients = Client.objects.filter(status="live").count()

        # 🟩 live in-house products
        live_products = Product.objects.filter(status="live").count()

        # 🟨 ongoing (both)
        ongoing_projects = (
            Client.objects.filter(status="ongoing").count() +
            Product.objects.filter(status="ongoing").count()
        )

        # 🟥 team counts
        team = {
            "it": TeamMember.objects.filter(department="it").count(),
            "digital_marketing": TeamMember.objects.filter(
                department="digital_marketing"
            ).count(),
            "sales": TeamMember.objects.filter(department="sales").count(),
        }

        return Response({
            "clients": live_clients,
            "products": live_products,
            "ongoing_projects": ongoing_projects,
            "team": team,
        })
