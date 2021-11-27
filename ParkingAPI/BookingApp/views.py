from django.shortcuts import render
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse

from BookingApp.models import ParkingLot, Parking_1, Parking_2, Parking_3, Parking_4
from BookingApp.serializers import ParkingLotSerializer, Parking_1Serializer, Parking_2Serializer, Parking_3Serializer, Parking_4Serializer
from datetime import datetime, timedelta

# Create your views here.

def requirements_check(customer_data):
    last_24hour_time = datetime.now() - timedelta(hours = 24)
    datetime_object = datetime.strptime(customer_data['BookingDate'],"%Y-%m-%d")
    print(last_24hour_time)
    print(datetime_object)
    if (last_24hour_time < datetime_object):
        return JsonResponse("You must book at least 24h in advance ", safe=False)


def oneBookingAday_check(park_wish_serializer,parking_data):
    print(park_wish_serializer['Lot_1'])
    print('Here 3')
    p = parking_data['LicensePlate']
    print (p)
    if ((p in park_wish_serializer['Lot_1']) or (p in park_wish_serializer['Lot_2']) or (p in park_wish_serializer['Lot_3']) or (p in park_wish_serializer['Lot_4'])): 
        print('YES-2')     
        return True


@csrf_exempt
def parkingApi(request):
    # Get the list of all parking lots for a given day with their status.
    # if a lot is booked it contains license plate; if it is available will be 
    # empty string.
    if request.method == 'GET':
        parking_data = JSONParser().parse(request)
        try:
            parking = ParkingLot.objects.filter(BookingDate=parking_data['BookingDate'])
            parking_serializer = ParkingLotSerializer(parking, many=True)
            return JsonResponse(parking_serializer.data, safe=False)
        except ParkingLot.DoesNotExist:
            return JsonResponse("Does not exist", safe=False)

        
        #parking = ParkingLot.objects.all()
        #parking_serializer = ParkingLotSerializer(parking,many=True)
        #parking = ParkingLot.objects.get(BookingDate=parking_data['BookingDate'])
        #parking_serializer=ParkingLotSerializer(parking,many=True)
        #if parking_serializer.is_valid():
        #    parking_serializer.save()
        #return JsonResponse(parking_serializer,safe=False)
        # return JsonResponse(parking_serializer.data,safe=False)
    #     
    elif request.method == 'PUT':
        parking_data = JSONParser().parse(request)
        print(parking_data['BookingDate'])
        parking = ParkingLot.objects.get(BookingDate=parking_data['BookingDate'])
        parking_serializer=ParkingLotSerializer(parking,data=parking_data)
        if parking_serializer.is_valid():
            parking_serializer.save()
            return JsonResponse("Update successfully", safe=False)
        return JsonResponse("Failed")

    elif request.method == 'POST':
        parking_data = JSONParser().parse(request)
        requirements_check(parking_data)
        # If there is no record with given date, we will create another one in 
        # ParkingLot table and assign Lot_1 to the customer. All other lots 
        # will be set to free at this moment. 
        if not(ParkingLot.objects.filter(BookingDate=parking_data['BookingDate']).exists()):
            p = ParkingLot.objects.create(BookingDate=parking_data['BookingDate'], Lot_1 = parking_data['DriverName']+": plate-"+parking_data['LicensePlate'] , Lot_2='', Lot_3='', Lot_4='')
            p_serializer=ParkingLotSerializer(data=p)
            if p_serializer.is_valid():
                p_serializer.save()
            p1 = Parking_1.objects.create(BookingDate=parking_data['BookingDate'],TimeOfBooking=datetime.now(),DriverName=parking_data['DriverName'], LicensePlate=parking_data['LicensePlate'])
            p1_serializer=Parking_1Serializer(data=p1)
            if p1_serializer.is_valid():
                p1_serializer.save()
            return JsonResponse("Booked successfully", safe=False)
        else: 
            print('Here 1')
            # If all lots are full for the required date, we will notify a customer
            # to select another day.
            parking = ParkingLot.objects.filter(BookingDate=parking_data['BookingDate'])
            parking_serializer = ParkingLotSerializer(parking,many=True)

                # But first to check if the customer already has a booking for that day
            if (oneBookingAday_check(parking_serializer.data[0],parking_data)):
                return JsonResponse("You can not book two parkig lots for the same day. ", safe=False)

            if ((parking_serializer.data[0]['Lot_1']!='' and parking_serializer.data[0]['Lot_2']!='' and parking_serializer.data[0]['Lot_3']!='' and parking_serializer.data[0]['Lot_4']!='')):
                return JsonResponse("We are full on that day. Please select another day.",safe=False)

                #return JsonResponse(parking_serializer.data, safe=False)
            return JsonResponse("Does not exist 1", safe=False)
            
            
            
            #park_wish = ParkingLot.objects.filter(BookingDate=parking_data['BookingDate'])
            #park_wish_serializer=ParkingLotSerializer(park_wish,many=True)
            #if park_wish_serializer.is_valid():
            #    oneBookingAday_check(park_wish_serializer,parking_data)
            #    print('Here 2')
            #    if not((park_wish_serializer['Lot_1']!='' and park_wish_serializer['Lot_2']!='' and park_wish_serializer['Lot_3']!='' and park_wish_serializer['Lot_4']!='')):
            #        return JsonResponse("We are full on that day. Please select another day.",safe=False)
        
        
        #return JsonResponse("Already exists",safe=False)
