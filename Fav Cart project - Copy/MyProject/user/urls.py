from django.urls import path
from .import views

urlpatterns=[
    path('',views.home),
    path('home/',views.home),
    path('index/',views.home),
    path('about/',views.about),
    path('contactus/',views.contactus),
    path('services/',views.services),
    path('myorders/',views.myorders),
    path('myprofile/',views.myprofile),
    path('signup/',views.signup),
    path('product/',views.product),
    path('viewdetails/',views.viewdetails),
    path('process/',views.process),
    path('logout/',views.logout),
    path('signin/',views.signin),
    path('cart/',views.cart),
]