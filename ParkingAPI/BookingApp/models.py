from django.db import models

# Create your models here.


class ParkingLot(models.Model):
    ParkingId = models.AutoField(primary_key=True)
    BookingDate = models.DateField()
    Lot_1 = models.CharField(max_length=200)
    Lot_2 = models.CharField(max_length=200)
    Lot_3 = models.CharField(max_length=200)
    Lot_4 = models.CharField(max_length=200)
    #Lot_1 = models.BooleanField(default=True)
    #Lot_2 = models.BooleanField(default=True)
    #Lot_3 = models.BooleanField(default=True)
    #Lot_4 = models.BooleanField(default=True)


class Parking_1(models.Model):
    ParkingId = models.AutoField(primary_key=True)
    BookingDate = models.DateField()
    TimeOfBooking = models.DateTimeField()
    DriverName = models.CharField(max_length=200)
    LicensePlate = models.CharField(max_length=10)


class Parking_2(models.Model):
    ParkingId = models.AutoField(primary_key=True)
    BookingDate = models.DateField()
    TimeOfBooking = models.DateTimeField()
    DriverName = models.CharField(max_length=200)
    LicensePlate = models.CharField(max_length=10)  


class Parking_3(models.Model):
    ParkingId = models.AutoField(primary_key=True)
    BookingDate = models.DateField()
    TimeOfBooking = models.DateTimeField()
    DriverName = models.CharField(max_length=200)
    LicensePlate = models.CharField(max_length=10)


class Parking_4(models.Model):
    ParkingId = models.AutoField(primary_key=True)
    BookingDate = models.DateField()
    TimeOfBooking = models.DateTimeField()
    DriverName = models.CharField(max_length=200)
    LicensePlate = models.CharField(max_length=10)          