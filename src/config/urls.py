"""
URL configuration for src project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin

from django.urls import path, include
from rest_framework import routers
from voting_api.views import (
    RestaurantViewSet,
    MenuViewSet,
    CompanyViewSet,
    EmployeeViewSet,
)
from voting_api.views import vote, get_vote_results

router = routers.DefaultRouter()
router.register(r"restaurants", RestaurantViewSet)
router.register(r"menus", MenuViewSet)
router.register(r"companies", CompanyViewSet)
router.register(r"employees", EmployeeViewSet)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(router.urls)),
    path("vote/", vote, name="vote"),
    path("get_vote_results/", get_vote_results, name="get_vote_results"),
    path("accounts/", include("rest_registration.api.urls")),
]
