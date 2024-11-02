from cgitb import text

from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from.models import file,encrypt,blockaes,blockdes,blockrc2,payment1
from visitor.models import Login,Registration
from Admin.models import Account
import base64
from Crypto.Cipher import AES,ARC2
from Crypto.Hash import SHA256
from Crypto import Random
from mimetypes import guess_type
from django.http import HttpResponse
from cloud import settings
from wsgiref.util import FileWrapper
from mimetypes import MimeTypes
import os
from django.conf import settings
from django.http import HttpResponse, Http404

from django.core.mail import send_mail
from django.conf import settings

from Crypto.Cipher import DES

from rc2 import *

from Crypto.Cipher import DES
import hashlib
import sys
import binascii
import Padding
import os

# Create your views here.
def upload(request):
    if request.method=="POST":
        fl=request.FILES["file"]
        #request.session["file"]=fl

        uname=request.session["uname"]
        status="pending"
        f=file()
        f.fname=fl
        f.uname=uname
        f.status=status
        f.save()

        return HttpResponse("<script>alert('file uploaded successfully');window.location='/block';</script>")
    else:
        template = loader.get_template("Upload.html")
        context = {}

        return HttpResponse(template.render(context, request))
def split(str, num):
    return [ str[i:i+num] for i in range(0, len(str), num) ]
def encrypt1(key, source, encode=True):
    key = SHA256.new(key).digest()  # use SHA-256 over our key to get a proper-sized AES key
    IV = Random.new().read(AES.block_size)  # generate IV
    encryptor = AES.new(key, AES.MODE_CBC, IV)
    padding = AES.block_size - len(source) % AES.block_size  # calculate needed padding
    s= bytes([padding]) * padding  # Python 2.x: source += chr(padding) * padding
    source=bytes(source)+s
    data = IV + encryptor.encrypt(source)  # store the IV at the beginning and encrypt
    return base64.b64encode(data).decode("latin-1") if encode else data

def decrypt1(key, source, decode=True):
    if decode:
        source = base64.b64decode(source.encode("latin-1"))
    key = SHA256.new(key).digest()  # use SHA-256 over our key to get a proper-sized AES key
    IV = source[:AES.block_size]  # extract the IV from the beginning
    decryptor = AES.new(key, AES.MODE_CBC, IV)
    data = decryptor.decrypt(source[AES.block_size:])  # decrypt
    padding = data[-1]  # pick the padding value from the end; Python 2.x: ord(data[-1])
    if data[-padding:] != bytes([padding]) * padding:  # Python 2.x: chr(padding) * padding
        raise ValueError("Invalid padding...")
    return data[:-padding]

def pad(text):
    while len(text) % 8 != 0:
        text += ' '
    return text
def encryptt(plaintext,key, mode):
	encobj = DES.new(key,mode)
	return(encobj.encrypt(plaintext))
def decryptt(ciphertext,key, mode):
	encobj = DES.new(key,mode)
	return(encobj.decrypt(ciphertext))

def encryptr(key, msg):
    encryped = []
    for i, c in enumerate(msg):
        key_c = ord(key[i % len(key)])
        msg_c = ord(c)
        encryped.append(chr((msg_c + key_c) % 500))
    return ''.join(encryped)
def decryptr(key, encryped):
    msg = []
    for i, c in enumerate(encryped):
        key_c = ord(key[i % len(key)])
        enc_c = ord(c)
        msg.append(chr((enc_c - key_c) % 500))
    return ''.join(msg)



def block(request):
    if request.method=="POST":
        text = request.POST.get("block1")
        text2=request.POST.get("block2")
        text3=request.POST.get("block3")
        request.session["key"]=request.POST.get("key")

        my_password = request.POST.get("key")
        my_data = text
        encrypted = encrypt1(my_password.encode("utf8"), my_data.encode("utf8"))
        decrypted = decrypt1(my_password.encode("utf8"), encrypted)


        #key = 'abcdefgh'
        #des = DES.new(key.encode("utf8"), DES.MODE_ECB)

        #padded_text = pad(text2)
        #encrypted_text = des.encrypt(padded_text.encode("utf8"))
        #de=des.decrypt(encrypted_text)

        plaintext = text2
        #key = hashlib.sha256(my_password.encode('utf-8')).digest()[:8]
        #plaintext = Padding.appendPadding(plaintext, blocksize=Padding.DES_blocksize)
        #ciphertext = encryptt(plaintext.encode('utf-8'), key, DES.MODE_ECB)
        #encrypted_text=binascii.hexlify(bytearray(ciphertext))
       # plaintext =decryptt(ciphertext, key, DES.MODE_ECB)
        #p=plaintext
        #plaintext = Padding.removePadding(p)
        #enc=encrypt_rc2(text3.encode('utf-8'),my_password.encode('utf-8'))

        offset = 5
        encrypted_text= encrypt1(my_password.encode("utf8"), plaintext.encode("utf8"))
        key=my_password
        encryptedr = encryptr(key,text3)
        decryptedr = decryptr(key,encryptedr)
        request.session["key"]=key















        lf=file.objects.last()
        f=lf.fname
        ff="media/"+str(f)
        fs=os.path.getsize(ff)
        request.session["fs"]=fs
        template = loader.get_template("encrypt.html")
        context = {'data':encrypted,'block2':encrypted_text,'block3':encryptedr}

        return HttpResponse(template.render(context, request))

    else:
        uname=request.session["uname"]
        d=file.objects.filter(uname=uname,status="pending")
        for j in d:
            d1=file.objects.get(id=j.id)

        fl=d1.fname
        request.session["fid"]=d1.id
        st=str(fl)
        f=open("media/"+st,"r")
        s=f.read()
        while (len(s) % 3) != 0:  # Keep adding whitespace until divisible by 3
         s += " "
        slice1, slice2, slice3 = split(s, int(len(s) / 3))
        template = loader.get_template("block.html")
        context = {'slice1':slice1,'slice2':slice2,'slice3':slice3}

        return HttpResponse(template.render(context, request))

def savefile(request):
    fs=request.session["fs"]
    fs1=int(fs)
    if fs1>1000:
        amt=fs1/1000
        amt1=int(amt)*100
        request.session["amount"]=amt1
        block1 = request.POST.get("eblock1")
        block2 = request.POST.get("eblock2")
        block3 = request.POST.get("eblock3")
        request.session["block1"]=block1
        request.session["block2"]=block2
        request.session["block3"]=block3
        return HttpResponse("<script>alert('Before uploading file you must pay an amount first');window.location='/payment';</script>")

    else:

        block1=request.POST.get("eblock1")
        block2=request.POST.get("eblock2")
        block3=request.POST.get("eblock3")
        password=request.session["key"]
        e=encrypt()
        id=request.session["fid"]
        e.fid=id
        e.uname=request.session["uname"]
        e.key=password
        e.status="pending"
        e.save()
        b1=blockaes()
        b1.encrypt=id
        b1.block=block1
        b1.save()
        b2=blockdes()
        b2.encrypt=id
        b2.block=block2
        b2.save()
        b3=blockrc2()
        b3.encrypt=id
        b3.block=block3
        b3.save()
        key=request.session["key"]
        subject = 'Thank you for registering to our site'
        message = 'your key value is ' + key
        email_from = settings.EMAIL_HOST_USER
        mailid = request.session["email"]
        recipient_list = [mailid, ]
        send_mail(subject, message, email_from, recipient_list)
        return HttpResponse("<script>alert('file uploaded successfully');window.location='/userh';</script>")
def download(request):

    uname=request.session["uname"]
    u = Registration.objects.filter(uname=uname)
    f = file.objects.filter(status='approve')
    e = encrypt.objects.filter(status='approve')
    template = loader.get_template("download.html")
    context = {'reg': u, 'file': f, 'encrypt': e}

    return HttpResponse(template.render(context, request))
def decryptfile(request,id):
    if request.method=="POST":
        key = request.POST.get("key")
        fid = request.session["fid"]
        f = encrypt.objects.get(fid=fid)
        if f.key == key:
            b1 = request.POST.get("eblock1")
            b2 = request.POST.get("eblock2")
            b3 = request.POST.get("eblock3")

            decrypted1 = decrypt1(key.encode("utf8"), b1)
            decrypted=str(decrypted1)
           # plaintext = text2
           # key = hashlib.sha256(key.encode('utf-8')).digest()[:8]
           # plaintext = Padding.appendPadding(plaintext, blocksize=Padding.DES_blocksize)
           # ciphertext = encryptt(plaintext.encode('utf-8'), key, DES.MODE_ECB)
           # encrypted_text = binascii.hexlify(bytearray(b2))
            #plaintext = decryptt(encrypted_text, key, DES.MODE_ECB)
            plaintext1= decrypt1(key.encode("utf8"), b2)
            plaintext=str(plaintext1)
            decryptedr = decryptr(key, b3)
            template = loader.get_template("viewencblock.html")
            context = {'block1':decrypted, 'block2':plaintext, 'block3': decryptedr}
            return HttpResponse(template.render(context, request))
        else:
            return HttpResponse("<script>alert('invalid key');window.location='/download';</script>")




    else:

        f = encrypt.objects.get(fid=id)
        b1 = blockaes.objects.get(encrypt=f.id)
        b2 = blockdes.objects.get(encrypt=f.id)
        b3 = blockrc2.objects.get(encrypt=f.id)
        request.session["eid"] = f.id
        request.session["fid"] = id
        template = loader.get_template("vieweblocks.html")
        context = {'block1': b1, 'block2': b2, 'block3': b3,'id':f}

        return HttpResponse(template.render(context, request))


def down(request):
    if request.method=="POST":
        b1=request.POST.get("block1")
        b2=request.POST.get("block2")
        b3=request.POST.get("block3")
        data=str(b1)+str(b2)+str(b3)
        fid=request.session["fid"]
        f=file.objects.get(id=fid)
        f1=f.fname
        st = str(f1)

        file_path = os.path.join(settings.MEDIA_ROOT, st)
        if os.path.exists(file_path):
            with open(file_path, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/vnd.text")
                response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
                return response
        raise Http404






        return HttpResponse("<script>alert('downloaded successfully');window.location='/download';</script>")



def userhome(request):
    context={}
    template=loader.get_template("userhome.html")
    return HttpResponse(template.render(context,request))


def phome(request):
    template = loader.get_template("paymenthome.html")
    context = {}
    return HttpResponse(template.render(context, request))
def paymentcon(request):

     cno = request.POST.get("cno")
     request.session["cno"] = cno
     sum = request.session["amount"]
     if (Account.objects.get(cno=cno)):
        x = Account.objects.get(cno=cno)
        context = {'sum': sum, 'card': x}
        template = loader.get_template("paymentcon.html")
        return HttpResponse(template.render(context, request))
     else:
        return HttpResponse("<script>alert('invalid card no');window.location='/payment';</script>")
def payment(request):
    #request.session["amount"]=request.POST.get("total")

    context = {}
    template = loader.get_template("payment.html")
    return HttpResponse(template.render(context, request))
def savepayment(request):
    uname=request.session["uname"]
    uid=Registration.objects.get(uname=uname)
    block1 = request.session["block1"]
    block2 = request.session["block2"]
    block3 = request.session["block3"]
    password = request.session["key"]
    amount=request.session["amount"]
    e = encrypt()
    id = request.session["fid"]
    e.fid = id
    e.uname = request.session["uname"]
    e.key = password
    e.status = "pending"
    e.save()
    b1 = blockaes()
    b1.encrypt = id
    b1.block = block1
    b1.save()
    b2 = blockdes()
    b2.encrypt = id
    b2.block = block2
    b2.save()
    b3 = blockrc2()
    b3.encrypt = id
    b3.block = block3
    b3.save()
    p=payment1()
    p.fid=id
    p.amt=amount
    p.save()
    cno=request.session["cno"]
    a=Account.objects.get(cno=cno)
    bal=int(a.amount)-int(amount)
    a.amount=bal
    a.save()
    key = request.session["key"]
    subject = 'Thank you for registering to our site'
    message = 'your key value is ' + key
    email_from = settings.EMAIL_HOST_USER
    mailid = request.session["email"]
    recipient_list = [mailid, ]
    send_mail(subject, message, email_from, recipient_list)
    return HttpResponse("<script>alert('file uploaded successfully');window.location='/userh';</script>")







