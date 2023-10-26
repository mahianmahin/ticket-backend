import json
import random

import qrcode
import stripe
from django.conf import settings
from django.contrib.auth.models import User
from django.core.serializers import serialize
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
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
        package_id = request.data['package_id']
        package_identifier = request.data['package_identifier']
        adult_count = request.data['adult_count']
        youth_count = request.data['youth_count']
        infant_count = request.data['infant_count']
        selected_date = request.data['date']

        if package_identifier == "E9":
            package_instance = BusPackages.objects.get(package_tag=package_id)
        elif package_identifier == "E8":
            package_instance = MuseumPackages.objects.get(package_tag=package_id)

        package_adult_price = package_instance.adult_price
        package_youth_price = package_instance.youth_price
        package_infant_price = package_instance.infant_price
        
        dynamic_price = (int(adult_count)*int(package_adult_price)) + (int(youth_count)*int(package_youth_price)) + (int(infant_count)*int(package_infant_price))
        package_unique_identifier = random.randint(100000, 999999)

        purchased_ticket_ins = PurchasedTickets(
            user = request.user.username,
            package = package_instance.title,
            total_price = dynamic_price,
            adults = adult_count,
            youths = youth_count,
            infants = infant_count,
            selected_date = selected_date,
            package_tag = package_instance.package_tag,
            package_unique_identifier = package_unique_identifier,
            
        )
        
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'eur',
                        'product_data': {
                            'name': request.data['title'],
                            'description': request.data['description'],
                            'images': [request.data['image']]
                        },
                        'unit_amount': dynamic_price * 100,
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url= f'{settings.SITE_URL}success/{package_unique_identifier}/',
            cancel_url= f'{settings.SITE_URL}cancel/',
        )

        return Response({'id': session.id})


# stripe payment webhook

from django.http import JsonResponse


@csrf_exempt
def stripe_webhook(request):
    payload = json.loads(request.body)
    event_type = payload['type']

    if event_type == 'checkout.session.completed':
        print('Payment Successful')

    elif event_type == 'checkout.session.async_payment_failed':
        print('Payment Failed')
        
    else:
        print(f'Unhandled event type: {event_type}')

    return JsonResponse({'status': 'success'})