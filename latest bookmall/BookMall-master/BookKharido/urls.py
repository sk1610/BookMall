from django.contrib import admin
from django.urls import path
from BookKharido import views

urlpatterns = [
    path("",views.index,name="home"),
    path("about",views.about,name="about"),
    path("contact",views.contact,name="contact"),
    path("login",views.login,name="login"),
    path("signup",views.signup,name="signup"),
    path("logout",views.logout,name="logout"),
    path("bookings",views.bookings,name="bookings"),
    path("otp",views.otp,name="otp"),
    path("sell",views.sell,name="sell"),
    path("cartbtn",views.cartbtn,name="cartbtn"),
    path("payment",views.payment,name="payment"),
    path("search",views.search,name="search"),
    path("checkout",views.checkout,name="checkout"),
    path("book/<int:bookid>",views.bookpager,name="bookpager")
]