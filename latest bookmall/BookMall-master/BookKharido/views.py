from django.shortcuts import render,HttpResponse,redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
import base64
import re
from math import ceil

from BookShop.settings import RAZORPAY_API_KEY, RAZORPAY_API_SECRET_KEY
from .models import book_table, Orders
from django.core.mail import send_mail
from django import template
import wikipedia
import json
import random
import string
from django.conf import settings
import razorpay
global price



# Create your views here.
def searchMatch(query,item):
    if query in item.book_name.lower() or query in item.book_category.lower() or query in item.book_subcategory.lower() or query in item.book_author.lower() or query in item.book_category.title() or query in item.book_author.title() :
        return True
    else:
        return  False

def search(request):
    query=request.GET.get('search')
    prods = []
    prod_cat = book_table.objects.values('book_category')
    categories = set(item['book_category'] for item in prod_cat)
    for cate in categories:
        prodtemp = book_table.objects.filter(book_category=cate)
        prod=[item for item in prodtemp if searchMatch(query,item)]
        n = len(prod)
        slides = n // 4 + ceil((n % 4) / 4)
        if len(prod)!=0:
             prods.append([prod, range(1, slides), slides])
    params = {'allProduct': prods}
    return render(request, 'index.html', params)


def logout(request):
    auth.logout(request)
    return redirect('/')

def sell(request):
    return render(request,'sell.html')

def bookings(request):
       dests=Orders.objects.all()
       return render(request,'history.html',{'dests':dests})

def payment(request):
    dests = Orders.objects.all()
    client = razorpay.Client(auth=(RAZORPAY_API_KEY, RAZORPAY_API_SECRET_KEY))
    order_amount = 50000
    order_currency = 'INR'
    payment_order=client.order.create(dict(amount=order_amount, currency=order_currency, payment_capture=1))
    payment_order_id=payment_order['id']
    context={
       'amount':order_amount, 'api_key':RAZORPAY_API_KEY,'order_id':payment_order_id,'dests':dests
    }

    return render(request,'payment.html',context)


def checkout(request):
    if request.method=="POST":
        items_json= request.POST.get('itemsJson', '')
        name=request.POST.get('name', '')
        email=request.POST.get('email', '')
        address=request.POST.get('address', '')
        city=request.POST.get('city', '')
        state=request.POST.get('state', '')
        zip_code=request.POST.get('zip_code', '')
        price=request.POST.get('price', '')
        phone=request.POST.get('phone', '')
        print(name)
        print(state)
        print(price)
        #price=request.POST.get('price', '')

        order = Orders(items_json= items_json, name=name, email=email, address= address, city=city, state=state, zip_code=zip_code, phone=phone,price=price)
        order.save()
        thank=True
        id=order.order_id
        return render(request, 'checkout.html', {'thank':thank, 'id':id})
    return render(request, 'checkout.html')

def index(request):
    # print("hello")
    # print(len(products))
    prods = []
    prod_cat = book_table.objects.values('book_category')
    categories = set(item['book_category'] for item in prod_cat)
    for cate in categories:
        prod = book_table.objects.filter(book_category = cate)
        n = len(prod)
        slides = n//4 + ceil((n%4)/4)
        prods.append([prod,range(1,slides),slides])
    params = {'allProduct' : prods}
    return render(request,'index.html',params)

def about(request):
    return render(request,'about.html')

def contact(request):
    return render(request,'contact.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            print("done done ")
            auth.login(request, user)
            return redirect("/")
        else:
            print("not valid")
            messages.info(request ,"invalid credentials")
            return redirect('login')
    else:
        return render(request,'login.html')

def otp(request):
    if(request.method == 'POST'):
        onetime = request.POST['Onetimepass']
        if(onetime == otpass):
            x = User.objects.create_user(username=name, email=email, password=password)
            x.save()
            return redirect('/login')
    return redirect('/signup')

def signup(request):
    if request.method == 'POST':
        global name, email, password, otpass
        name = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['cpassword']
        otpass = createOTP()
        subject = 'Confirm Your EmailId'
        message = f'Your One Time Password is {otpass}'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email]
        send_mail( subject, message, email_from, recipient_list )
        return render(request,'otp.html')
    else:
        return render(request, 'signup.html')


def cartbtn(request):
    if (request.method == 'POST'):
        cartproduct = request.POST.get('productid')
        cartbooks = json.loads(cartproduct)
        quantity = cartbooks.values()
        books = []
        for item in cartbooks:
            product = book_table.objects.filter(id=item[4::1]).values()[0]
            books.append(product)
        bookqty = zip(books, quantity)
        return render(request, "cartpage.html", {'cartbooks': bookqty})
    return HttpResponse("Please Login to continue!!")



def bookpager(request,bookid):
    book = book_table.objects.filter(id=bookid)
    print(book)
    # wiki = wikipedia.page(book[0].book_name)
    text = wikipedia.summary(book[0].book_name,sentences=3)
    return render(request,'bookpage.html',{'book': book[0],'description' : text})

register = template.Library()
@register.simple_tag()
def multiply(qty, unit_price, *args, **kwargs):
    # you would need to do any localization of the result here
    return qty * unit_price


# Create functions here

def createOTP():
    letter = string.ascii_letters + string.digits
    opass = ''
    for i in range(6):    #First website of my own
        opass = opass + ''.join(random.choice(letter))
    return opass


def decode_base64(data, altchars=b'+/'):
    """Decode base64, padding being optional.

    :param data: Base64 data as an ASCII byte string
    :returns: The decoded byte string.

    """
    data = re.sub(rb'[^a-zA-Z0-9%s]+' % altchars, b'', data)  # normalize
    missing_padding = len(data) % 4
    if missing_padding:
        data += b'='* (4 - missing_padding)
    return base64.b64decode(data, altchars)