import logging
from datetime import datetime
from typing import Any, Dict, Union, List

from django.http import HttpResponse, JsonResponse
from rest_framework import status, viewsets
from rest_framework.parsers import JSONParser


from .models import Company, Employee, Menu, Results, Restaurant, Voting
from .serializers import (
    MenuSerializer,
    ResultsSerializer,
    RestaurantSerializer,
    EmployeeSerializer,
    CompanySerializer,
)

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class RestaurantViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing restaurant instances.
    """

    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer


class MenuViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing menu instances.
    """

    queryset = Menu.objects.all()
    serializer_class = MenuSerializer


class EmployeeViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """

    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class CompanyViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """

    queryset = Company.objects.all()
    serializer_class = CompanySerializer


def vote(request) -> JsonResponse:
    """
    Api to vote for a menu
    """
    data: Dict[str, Any] = JSONParser().parse(request)
    version: str = request.headers.get("Version", "")

    if not request.user:
        return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

    employee = Employee.objects.get(user=request.user)

    if version == "1.0":
        menu_id: int = data.get("menu_id", 0)
        menu: Union[None, Menu] = Menu.objects.filter(id=menu_id).first()

        if menu:
            voting, _ = Voting.objects.get_or_create(
                date=datetime.now(),
                company=employee.company,
            )
            result, _ = Results.objects.get_or_create(voting=voting, menu=menu)
            result.points += 3
            result.save()
            logging.info(f"Vote for menu_id: {menu_id}")
        else:
            logging.info(f"No Menu found with menu_id: {menu_id}")
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

    elif version == "2.0":
        menu_ids: List[str] = ["menu_id_1", "menu_id_2", "menu_id_3"]
        results_points: List[int] = [3, 2, 1]
        for i, menu_id in enumerate(menu_ids):
            m_id: int = data.get(menu_id, 0)
            menu: Union[None, Menu] = Menu.objects.filter(id=m_id).first()
            if menu:
                voting, _ = Voting.objects.get_or_create(
                    date=datetime.now(),
                    company=employee.company,
                )
                result, _ = Results.objects.get_or_create(voting=voting, menu=menu)
                result.points += results_points[i]
                result.save()
                logging.info(f"Vote for menu_id: {menu_id}")
            else:
                logging.info(f"No Menu found with menu_id: {menu_id}")
                return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
    else:
        logging.info(f"Invalid version: {version}")
        return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

    return JsonResponse({"success": True})


def get_vote_results(request) -> JsonResponse:
    """
    API to return the top 3 voted menus.
    """

    if not request.user:
        return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

    employee = Employee.objects.get(user=request.user)

    voting = Voting.objects.filter(
        date=datetime.now(), company=employee.company
    ).first()

    if not voting:
        logging.info(f"No voting found for {employee.company}")
        return JsonResponse({"success": False})

    results = Results.objects.filter(voting=voting).order_by("-points").first()
    serializer = ResultsSerializer(results)
    return JsonResponse(serializer.data, safe=False)
