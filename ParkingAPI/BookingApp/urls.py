from django.conf.urls import url
from BookingApp import views

urlpatterns=[
    url(r'^parking$',views.parkingApi),
    url(r'^parking/([0-9]+)$',views.parkingApi),
    url(r'^parking/2021-11-26',views.parkingApi)
]
