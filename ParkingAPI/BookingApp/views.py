from django.shortcuts import render
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse

from BookingApp.models import ParkingLot, Parking_1, Parking_2, Parking_3, Parking_4
from BookingApp.serializers import ParkingLotSerializer, Parking_1Serializer, Parking_2Serializer, Parking_3Serializer, Parking_4Serializer
from datetime import datetime, timedelta, date

# Create your views here.

def requirements24_check(customer_data):
    #last_24hour_time = datetime.now() - timedelta(hours = 24)
    datetime_object = datetime.strptime(customer_data['BookingDate'],"%Y-%m-%d").date()
    if not(datetime_object > date.today()):
        return True

def oneBookingAday_check(park_wish_serializer,parking_data):
    print(park_wish_serializer['Lot_1'])
    print('Here 3')
    p = parking_data['LicensePlate']
    print (p)
    if ((p in park_wish_serializer['Lot_1']) or (p in park_wish_serializer['Lot_2']) or (p in park_wish_serializer['Lot_3']) or (p in park_wish_serializer['Lot_4'])): 
        print('YES-2')     
        return True

def bookParkingLot(parking_data):
    print(parking_data)
    parking = ParkingLot.objects.get(BookingDate=parking_data['BookingDate'])
    parking_serializer = ParkingLotSerializer(parking, many=True)
    new_park = parking_data['DriverName']+"; plate-"+parking_data['LicensePlate']+"; TimeOfBooking- "+str(datetime.now())
    #print(new_park)
    if (parking.Lot_2 ==''):
        parking.Lot_2 = new_park
        parking.save()
    elif (parking.Lot_3 ==''):
        print('here123')
        parking.Lot_3 = new_park
        print(parking.Lot_3)
        parking.save()
    else:
        print('here126')
        parking.Lot_4 = new_park
        parking.save()

    parking_serializer = ParkingLotSerializer(data=parking, many=True)
    if parking_serializer.is_valid():
        parking_serializer.save()
    return JsonResponse("Done nicelly", safe=False)
    


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

    elif request.method == 'POST':
        parking_data = JSONParser().parse(request)
        # If there is no record with given date, we will create another one in 
        # ParkingLot table and assign Lot_1 to the customer. All other lots 
        # will be set to free at this moment. 
        if not(ParkingLot.objects.filter(BookingDate=parking_data['BookingDate']).exists()):
            if (requirements24_check(parking_data)):
                return JsonResponse("You must book at least 24h in advance ", safe=False)

            p = ParkingLot.objects.create(BookingDate=parking_data['BookingDate'], Lot_1 = parking_data['DriverName']+"; plate-"+parking_data['LicensePlate']+"; TimeOfBooking - "+str(datetime.now()), Lot_2='', Lot_3='', Lot_4='')
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

            if ((parking_serializer.data[0]['Lot_1']!='' and parking_serializer.data[0]['Lot_2']!='' and parking_serializer.data[0]['Lot_3']!='' and parking_serializer.data[0]['Lot_4']!='')):
                return JsonResponse("We are full on that day. Please select another day.",safe=False)

                # Check if the customer already has a booking for that day
            if (oneBookingAday_check(parking_serializer.data[0],parking_data)):
                return JsonResponse("You can not book two parkig lots for the same day. ", safe=False) 

                # Check if the customer already booked within 24 hrs
            if (requirements24_check(parking_data)):
                return JsonResponse("You must book at least 24h in advance ", safe=False)
    
            if (bookParkingLot(parking_data)):
                return JsonResponse("Booked a bay successfully", safe=False)
            
    else:
        return JsonResponse("DONE", safe=False)

             