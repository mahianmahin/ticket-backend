import json

from django.core.serializers import serialize
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import *
from .serializers import *


def process_query(model_query):
    return json.loads(serialize("json", model_query))

@api_view(['GET'])
def hero_image(request):
    hero_image = process_query(HeroImage.objects.all())
    print(hero_image)

    return Response({
        'status': status.HTTP_200_OK,
        'data': {
            'hero_image': hero_image 
        }
    })

@api_view(['GET'])
def packages(request):
    bus_packages = BusPackages.objects.all()
    bus_serializer = BusPackagesSerializer(bus_packages, many=True)

    museum_serializer = MuseumPackagesSerializer(MuseumPackages.objects.all(), many=True)


    return Response({
        'status': status.HTTP_200_OK,
        'bus_data': bus_serializer.data,
        'museum_data': museum_serializer.data
    })

@api_view(['GET'])
def package(request, req_status, tag):
    if req_status == "E8":
        museum_package = MuseumPackages.objects.get(package_tag=tag)
        print(museum_package.dates.all())
        serializer = MuseumPackagesSerializer2(museum_package)
        print(museum_package)
    elif req_status == "E9":
        bus_package = BusPackages.objects.get(package_tag=tag)
        serializer = BusPackagesSerializer(bus_package)
        

    return Response({
        'status': status.HTTP_200_OK,
        'data': serializer.data
    })

@api_view(['GET'])
def get_dates(request, id):
    # dates = Date.
    pass

    return Response({
        "status": status.HTTP_200_OK
    })