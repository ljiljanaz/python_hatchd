from rest_framework import serializers
from BookingApp.models import ParkingLot, Parking_1,Parking_2, Parking_3, Parking_4

class ParkingLotSerializer(serializers.ModelSerializer):
    class Meta:
        model=ParkingLot
        fields=('ParkingId','BookingDate','Lot_1','Lot_2','Lot_3','Lot_4')


class Parking_1Serializer(serializers.ModelSerializer):
    class Meta:
        model=Parking_1
        fields=('ParkingId','BookingDate','TimeOfBooking','DriverName','LicensePlate')
                

class Parking_2Serializer(serializers.ModelSerializer):
    class Meta:
        model=Parking_2
        fields=('ParkingId','BookingDate','TimeOfBooking','DriverName','LicensePlate')
                  

class Parking_3Serializer(serializers.ModelSerializer):
    class Meta:
        model=Parking_3
        fields=('ParkingId','BookingDate','TimeOfBooking','DriverName','LicensePlate')
                    

class Parking_4Serializer(serializers.ModelSerializer):
    class Meta:
        model=Parking_4
        fields=('ParkingId','BookingDate','TimeOfBooking','DriverName','LicensePlate')
