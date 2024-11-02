from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from.models import Login,Registration
from django.http import JsonResponse
# Create your views here.
def login(request):
    if request.method=="POST":
        uname = request.POST.get("name")
        pwd = request.POST.get("password")
        if (Login.objects.filter(uname=uname, pwd=pwd)):
            l = Login.objects.filter(uname=uname, pwd=pwd)
            for i in l:
                status=i.status
                role = i.role
            if (role == "admin"):
                template = loader.get_template("AdminMaster.html")
                context = {}

                return HttpResponse(template.render(context, request))
            elif(role=="user"):
                if(status=="0"):
                    return HttpResponse("<script>alert('access denied!! ');window.location='/login';</script>")
                else:
                    request.session["uname"]=uname
                    r=Registration.objects.get(uname=uname)
                    request.session["email"]=r.email
                    template = loader.get_template("userhome.html")
                    context = {}

                    return HttpResponse(template.render(context, request))





        else:
            return HttpResponse("<script>alert('invalid username or password');window.location='/login';</script>")


    else:
        template = loader.get_template("login.html")
        context = {}
        return HttpResponse(template.render(context, request))
def admin(request):
    template = loader.get_template("AdminMaster.html")
    context = {}
    return HttpResponse(template.render(context, request))
def logout(request):
    try:
        del request.session["uid"]
    except:
        pass
    context={}
    template = loader.get_template("login.html")
    return HttpResponse(template.render(context, request))
def reg(request):
    if request.method=="POST":
        name = request.POST.get("Name")
        gen = request.POST.get("gender")
        hname=request.POST.get("HouseName")
        loc = request.POST.get("Location")
        zip = request.POST.get("ZipCode")
        email=request.POST.get("Email")
        phno=request.POST.get("Phone")
        uname=request.POST.get("Username")
        pwd=request.POST.get("Password")
        l=Login()
        l.pwd=pwd
        l.uname=uname
        l.role="user"
        l.status="0"
        l.save()
        r=Registration()
        r.name=name
        r.gender=gen
        r.hname=hname
        r.location=loc
        r.zipcode=zip
        r.email=email
        r.phno=phno
        r.uname=uname
        r.save()
        return HttpResponse("<script>alert('registration completed ');window.location='/reg/';</script>")





    else:
        context = {}
        template = loader.get_template("registration.html")
        return HttpResponse(template.render(context, request))



def unamecheck(request,uname):
    uname = uname
    l = Registration.objects.all()
    if l.uname==uname:
        return HttpResponse("<script>alert('already exist ');window.location='/reg/';</script>")
    else:
        return HttpResponse("<script>alert('registration completed ');window.location='/reg/';</script>")


def umaster(request):
    context = {}
    template = loader.get_template("UserMaster.html")
    return HttpResponse(template.render(context, request))

def index(request):
    context = {}
    template = loader.get_template("index.html")
    return HttpResponse(template.render(context, request))

