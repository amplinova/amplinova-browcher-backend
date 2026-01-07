
from django.contrib import admin

from .models import Client
admin.site.register(Client)

from .models import Product
admin.site.register(Product)

from .models import TeamMember
admin.site.register(TeamMember) 