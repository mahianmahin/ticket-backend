import json
import random
from io import BytesIO

import qrcode
import stripe
from django.conf import settings
from django.contrib.auth.models import User
from django.core.files import File
from django.core.serializers import serialize
from django.db import IntegrityError
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from PIL import Image
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
    folders = TicketFoldersSerializer(TicketFolders.objects.all(), many=True)
    museum_serializer = MuseumPackagesSerializer(MuseumPackages.objects.all(), many=True)


    return Response({
        'status': status.HTTP_200_OK,
        'bus_data': bus_serializer.data,
        'museum_data': museum_serializer.data,
        'folders': folders.data
    })

@api_view(['GET'])
def packages_list(request, id):
    bus_packages = BusPackages.objects.filter(folder_id=id)
    bus_serializer = BusPackagesSerializer(bus_packages, many=True)
    museum_serializer = MuseumPackagesSerializer(MuseumPackages.objects.all(), many=True)


    return Response({
        'status': status.HTTP_200_OK,
        'bus_data': bus_serializer.data,
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

@api_view(['GET'])
def utilities(request):
    utilities = Utilities.objects.all()
    utility_serializer = UtilitiesSerializer(utilities, many=True)

    return Response({
        'status':status.HTTP_200_OK,
        'data': utility_serializer.data
    })


@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def success_page(request, unique_identifier):
    package_ins = PurchasedTickets.objects.get(package_unique_identifier=unique_identifier)

    return Response({
        'url': package_ins.qr_code.url
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

test_secret_key = "sk_test_51O7GYsDBCudQgM49KyBAdFWQiPTP1KVWExXAmdqLNnFtBtiomOoVcDOWPpZQv09bthGoPvlqZJ8vc7SHEoE2agZB00nloJXZ2g"
live_secret_key = "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"

# stripe secret key
stripe.api_key = live_secret_key


# qr_code generation


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
            qr_content = f"{settings.SITE_URL}{package_unique_identifier}/"
        )

        purchased_ticket_ins.save()
        
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
            success_url = f'{settings.SITE_URL}success/{package_unique_identifier}/',
            cancel_url = f'{settings.SITE_URL}cancel/',
            client_reference_id = package_unique_identifier,
        )

        return Response({'id': session.id})


# stripe payment webhook

from django.http import JsonResponse


@csrf_exempt
def stripe_webhook(request):
    payload = json.loads(request.body)
    event_type = payload['type']

    if event_type == 'checkout.session.completed':
        session = payload['data']['object']
        client_reference_id = session.get('client_reference_id')
        
        purchased_tickets_ins = PurchasedTickets.objects.get(package_unique_identifier=client_reference_id)
        purchased_tickets_ins.paid = True

        purchased_tickets_ins.save()

    elif event_type == 'checkout.session.async_payment_failed':
        print('Payment Failed')
        
    else:
        print(f'Unhandled event type: {event_type}')

    return JsonResponse({'status': 'success'})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard(request):
    packages_ins = PurchasedTickets.objects.filter(user=request.user.username,)
    serializer = PurchasedTicketsSerializer(packages_ins, many=True)
    print(serializer.data)

    return Response({
        'data': serializer.data
    })

@api_view(['GET'])
def authenticate_qr_codes(request, code):
    # if request.user.is_staff:
    ticket_ins = PurchasedTickets.objects.get(package_unique_identifier=code)
    serializer = PurchasedTicketsSerializer(ticket_ins)

    agent_objects = AgentProperties.objects.all()
    agent_list = [obj.agent.username for obj in agent_objects]

    if ticket_ins.qr_code_scanned:
        return Response({
            'status': status.HTTP_200_OK,
            'data': serializer.data,
            'claimed': True,
            'agent_list': agent_list,
            'msg': 'This ticket is already claimed!'
        })
        
    else:
        # ticket_ins.qr_code_scanned = True
        # ticket_ins.save()

        return Response({
            'status': status.HTTP_200_OK,
            'data': serializer.data,
            'claimed': False,
            'agent_list': agent_list,
            'msg': 'Ticket is not claimed!'
        })

@api_view(['GET'])
def claim_ticket(request, code, agent_username, agent_code):

    user = User.objects.get(username=agent_username)
    agent_property = AgentProperties.objects.get(agent=user.id)

    if agent_property.code == int(agent_code):
        ticket_ins = PurchasedTickets.objects.get(package_unique_identifier=code)
        ticket_ins.qr_code_scanned = True
        ticket_ins.save()

        return Response({
            'status': status.HTTP_200_OK,
            'success': True
        })
    
    else:
        return Response({
            'status': status.HTTP_200_OK,
            'success': False
        })