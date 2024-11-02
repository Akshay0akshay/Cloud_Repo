from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from visitor.models import Login,Registration
from User.models import file,encrypt,blockaes,blockdes,blockrc2,payment1
from.models import Branch,Bank,Account
from django.http import JsonResponse

# Create your views here.
def viewuser(request):
    u=Registration.objects.all()
    l=Login.objects.filter(status=0)
    template = loader.get_template("ApproveUser.html")
    context = {'data':u,'log':l}

    return HttpResponse(template.render(context, request))
def approve(request,id):
    l=Login.objects.get(id=id)
    l.status="1"
    l.save()
    return HttpResponse("<script>alert('approved successfully');window.location='/approveuser';</script>")
def reject(request,id):
    l=Login.objects.get(id=id)
    l.status="2"
    l.save()
    return HttpResponse("<script>alert('rejected successfully');window.location='/approveuser';</script>")
def viewfile(request):
    u=Registration.objects.all()
    f=file.objects.filter(status='pending')
    e=encrypt.objects.filter(status='pending')

    template = loader.get_template("approvefiles.html")
    context = {'reg': u, 'file': f,'encrypt':e}

    return HttpResponse(template.render(context, request))
def viewefile(request,id):
    f=encrypt.objects.get(fid=id)
    b1=blockaes.objects.get(encrypt=f.id)
    b2=blockdes.objects.get(encrypt=f.id)
    b3=blockrc2.objects.get(encrypt=f.id)
    request.session["eid"]=f.id
    request.session["fid"]=id
    template = loader.get_template("viewblocks.html")
    context = {'block1': b1, 'block2': b2, 'block3': b3}

    return HttpResponse(template.render(context, request))
def verify(request):
    fid=request.session["fid"]
    eid=request.session["eid"]
    f=file.objects.get(id=fid)
    f.status='approve'
    f.save()
    e=encrypt.objects.get(id=eid)
    e.status='approve'
    e.save()
    return HttpResponse("<script>alert('approved successfully');window.location='/approvefile';</script>")
def banking(request):
    context = {}
    template = loader.get_template("banking.html")
    return HttpResponse(template.render(context, request))
def addbank(request):
    if request.method == "POST":

        bname=request.POST.get("bname")
        logo=request.FILES["logo"]

        s1=Bank.objects.all()
        for i in s1:
            if(i.bname == bname):
                return HttpResponse("<script>alert('already exist');window.location='/addbank';</script>")
        else:
            s=Bank()
            s.bname=bname
            s.logo=logo
            s.save()
            return HttpResponse("<script>alert('bank name added successfully');window.location='/addbank';</script>")
    else:
        context = {}
        template = loader.get_template("AddBank.html")
        return HttpResponse(template.render(context, request))
def addaccount(request):
    if request.method == "POST":
        bname = request.POST.get("drpbank")
        bankid = Bank.objects.get(id=bname)
        brname = request.POST.get("drpbranch")
        branchid = Branch.objects.get(id=brname)
        cname = request.POST.get("cname")
        cno = request.POST.get("cno")
        cvv = request.POST.get("cvv")
        year = request.POST.get("year")
        month = request.POST.get("month")
        amount = request.POST.get("amount")
        s = Account()

        s.cname = cname
        s.cno = cno
        s.cvv = cvv
        s.amount = amount
        s.year = year
        s.month = month
        s.bname = bankid.id
        s.branch = branchid.id
        s.save()
        return HttpResponse("<script>alert('account added successfully');window.location='/addaccount';</script>")
    else:
        b = Bank.objects.all()
        template = loader.get_template("AddAccount.html")
        context = {'bank': b}
        return HttpResponse(template.render(context, request))
def brnch(request):
    if (request.method == 'GET' and request.GET.get('q') != None):
        did = request.GET.get('q')
        l = Branch.objects.filter(bname=did).values()
        return JsonResponse(list(l), safe=False)


def addbranch(request):
    if request.method=="POST":
        bn=request.POST.get("drpbname")
        bid=Bank.objects.get(id=bn)
        brname=request.POST.get("branch")
        addr = request.POST.get("addr")
        ifsc = request.POST.get("ifsc")
        email = request.POST.get("email")
        phno = request.POST.get("phno")
        s=Branch()
        s.branch=brname
        s.address=addr
        s.email=email
        s.phone=phno
        s.ifsc=ifsc
        s.bname=bid.id
        s.save()
        return HttpResponse("<script>alert('branch added successfully');window.location='/addbranch';</script>")
    else:
        s = Bank.objects.all()
        template = loader.get_template("AddBranch.html")
        context = {'bank': s}
        return HttpResponse(template.render(context, request))
def viewpayment(request):
    p=payment1.objects.raw("SELECT visitor_registration.name,user_payment1.*,user_file.fname,user_file.status from visitor_registration,user_payment1,user_file where visitor_registration.uname=user_file.uname and user_file.id=user_payment1.fid")
    template = loader.get_template("viewpayment.html")
    context = {'key': p}
    return HttpResponse(template.render(context, request))










