import json

import qrcode
import stripe
from django.conf import settings
from django.contrib.auth.models import User
from django.core.serializers import serialize
from django.db import IntegrityError
from rest_framework import status
from rest_framework.decorators import (api_view, parser_classes,
                                       permission_classes)
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import *
from .serializers import *


def process_query(model_query):
    return json.loads(serialize("json", model_query))

@api_view(['GET'])
def hero_image(request):
    hero_image = process_query(HeroImage.objects.all())

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
        serializer = MuseumPackagesSerializer2(museum_package)
        
    elif req_status == "E9":
        bus_package = BusPackages.objects.get(package_tag=tag)
        serializer = BusPackagesSerializer(bus_package)
        

    return Response({
        'status': status.HTTP_200_OK,
        'data': serializer.data
    })


@api_view(['POST'])
# @parser_classes([MultiPartParser])
def user_register(request):
    try:
        if request.method == "POST":
            user_ins = User(
                username = request.data['full_name'],
                email = request.data['email']
            )

            user_ins.set_password(request.data['password'])
            user_ins.save()

            return Response({
                'status': status.HTTP_200_OK,
                'registered': True
            })
    except IntegrityError as e:
        return Response({
            'status': status.HTTP_400_BAD_REQUEST,
            'error': f'{request.data["full_name"]} is already registered!'
        })
        
    except Exception as e:
        return Response({
            'status': status.HTTP_508_LOOP_DETECTED,
            'data': str(e)
        })
    
api_view(['GET'])
def qrcode(request):
    img = qrcode.make("test")
    img.save("/codes/img1.png")

    return Response({})

# stripe secret key
stripe.api_key = "sk_test_51JLudiCHMxzhWuhuG5YgutpTZ1yuhTTb6s3rWDlttErYKMfKI5K0LxcMylDP3Laq2eZ3PmvinzZfZl1Mh5fRmxrM00weRJKw1M"

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_checkout_session(request):
    if request.method == "POST":
        print(request.user)
        package_id = request.data['package_id']
        package_identifier = request.data['package_identifier']
        adult_count = request.data['adult_count']
        youth_count = request.data['youth_count']
        infant_count = request.data['infant_count']

        if package_identifier == "E9":
            package_instance = BusPackages.objects.get(package_tag=package_id)
        elif package_identifier == "E8":
            package_instance = MuseumPackages.objects.get(package_tag=package_id)

        package_adult_price = package_instance.adult_price
        package_youth_price = package_instance.youth_price
        package_infant_price = package_instance.infant_price
        
        dynamic_price = (int(adult_count)*int(package_adult_price)) + (int(youth_count)*int(package_youth_price)) + (int(infant_count)*int(package_infant_price))
        print(dynamic_price)

        # Create a Stripe Session with dynamic pricing in Euro (EUR)
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'eur',  # Currency code for Euro
                        # 'product': 'prod_OsXM0atVqBHgIX',
                        'product_data': {
                            'name': request.data['title'],  # Product name
                            'description': request.data['description'],
                            'images': [request.data['image']]
                        },
                        'unit_amount': dynamic_price * 100,  # Unit amount in cents (stripe expects amount in cents)
                    },
                    'quantity': 1,  # Quantity of the product (adjust as needed)
                },
            ],
            mode='payment',
            success_url= f'{settings.SITE_URL}success/',
            cancel_url= f'{settings.SITE_URL}cancel/',
        )

        return Response({'id': session.id})