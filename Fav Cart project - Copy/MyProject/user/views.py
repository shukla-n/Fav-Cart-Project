from django.shortcuts import render
from django.http import HttpResponse
from .models import *
import datetime
from django.db import connection


# Create your views here.
def home(req):


    cdata = category.objects.all().order_by('id')[0:6]
    pdata = products.objects.all().order_by('id')[0:80]
    noofitemsincart=addtocart.objects.all().count()
    print(noofitemsincart)

    return render(req, 'user/index.html', {"data": cdata, "prod": pdata,"noofitemsincart":noofitemsincart})


def about(req):
    return render(req, 'user/about.html')


def contactus(request):
    status = False
    if request.method == 'POST':
        a = request.POST.get("name", "")
        b = request.POST.get("mobile", "")
        c = request.POST.get("email", "")
        d = request.POST.get("msg", "")
        x = contact(name=a, email=c, contact=b, message=d)
        x.save()
        status = True
        # return HttpResponse("<script>alert('Thanks for enquiry..');window.location.href='/user/contactus/'</script>")

    return render(request, 'user/contactus.html', {'S': status})


def services(req):
    return render(req, 'user/services.html')


def myorders(request):
    userid=request.session.get('userid')
    oid=request.GET.get('oid')
    orderdata=""
    if userid:
        cursor=connection.cursor()
        cursor.execute("select o.*,p.* from user_order o,user_products p where o.pid=p.id and o.userid='"+str(userid)+"'")
        orderdata=cursor.fetchall()
        if oid:
            result=order.objects.filter(id=oid,userid=userid)
            result.delete()
            return HttpResponse("<script>alert('Your order has been cancelled..');window.location.href='/user/myorders'</script>")

    return render(request, 'user/myorders.html',{"pendingorder":orderdata})


def myprofile(req):
    return render(req, 'user/myprofile.html')


def product(req):
    cdata = category.objects.all().order_by('-id')
    x = req.GET.get('abc')

    if x is not None:
        pdata = products.objects.filter(category=x)
    else:
        pdata = products.objects.all().order_by('id')
    print(x)

    return render(req, 'user/product.html', {"cat": cdata, "prod": pdata})


def signup(req):
    status = False
    if req.method == 'POST':
        name = req.POST.get("name", "")
        email = req.POST.get("email", "")
        mobile = req.POST.get("mobile", "")
        password = req.POST.get("passwd", "")
        address = req.POST.get("address", "")
        picname = req.FILES['fu']
        d = profile.objects.filter(email=email)

        if d.count() > 0:
            return HttpResponse(
                "<script>alert('You are already registered..');window.location.href='/user/signup/'</script>")
        else:
            res = profile(name=name, email=email, mobile=mobile, passwd=password, address=address, ppic=picname)
            res.save()
            return HttpResponse(
                "<script>alert('You are registered successfully..');window.location.href='/user/signup/'</script>")

        # return HttpResponse("<script>alert('Thanks For SignUp..');window.location.href='/user/signup/';</script>")
    return render(req, 'user/signup.html')


def signin(request):
    if request.method == 'POST':

        uname = request.POST.get("uname")
        passwd = request.POST.get("passwd")
        checkuser = profile.objects.filter(email=uname, passwd=passwd)
        if (checkuser):
            request.session['userid'] = uname
            return HttpResponse("<script>alert('Logged In Successfully');window.location.href='/user/signin';</script>")

        else:
            return HttpResponse(
                "<script>alert('UserID or Password is Incorrect');window.location.href='/user/signin';</script>")
    return render(request, 'user/signin.html')


def viewdetails(request):
    a = request.GET.get('msg')

    data = products.objects.filter(id=a)

    return render(request, 'user/viewdetails.html', {"d": data})


def process(request):
    userid = request.session.get('userid')
    pid = request.GET.get('pid')
    btn = request.GET.get('bn')
    print(userid, pid, btn)
    if userid is not None:
        if btn == 'cart':
            checkcartitem = addtocart.objects.filter(pid=pid, userid=userid)
            if checkcartitem.count() == 0:
                addtocart(pid=pid, userid=userid, status=True, cdate=datetime.datetime.now()).save()
                return HttpResponse("<script>alert('You item is successfully added in cart..');window.location.href='/user/home/'</script>")

            else:
                return HttpResponse("<script>alert('This items is already added in Cart...');window.location.href='/user/home/'</script>")
        elif btn == 'order':
            order(pid=pid, userid=userid, remarks="Pending", status=True, odate=datetime.datetime.now()).save()
            return HttpResponse("<script>alert('Your order have confirmed....');window.location.href='/user/myorders/'</script>")

        elif btn=='orderfromcart':
            res=addtocart.objects.filter(pid=pid,userid=userid)
            res.delete()
            order(pid=pid,userid=userid,remarks="Pending",status=True,odate=datetime.datetime.now()).save()
            return HttpResponse("<script>alert('Your order have confirmed....');window.location.href='/user/myorders/'</script>")
        return render(request, 'user/process.html', {"alreadylogin": True})



    else:
        return HttpResponse("<script>window.location.href='/user/signin/'</script>")


def logout(request):
    del request.session['userid']
    return HttpResponse("<script>window.location.href='/user/home/'</script>")


def cart(request):
    if request.session.get('userid'):
        userid = request.session.get('userid')
        cursor = connection.cursor()
        cursor.execute(
            "select c.*,p.* from user_addtocart c, user_products p where p.id=c.pid and userid='" + str(userid) + "'")
        cartdata = cursor.fetchall()
        pid = request.GET.get('pid')
        if request.GET.get('pid'):
            res = addtocart.objects.filter(id=pid, userid=userid)
            res.delete()
            return HttpResponse(
                "<script>alert('Your product has been removed successfully');window.location.href='/user/cart/'</script>")

    return render(request, 'user/cart.html', {"cart": cartdata})
