from django.urls import path
import User.views
import visitor.views

urlpatterns = [

    path('upload/',User.views.upload,name='upload'),
    path('block/',User.views.block,name='block'),
    path('umaster/',visitor.views.umaster,name='umaster'),
    path('encrypt/',User.views.savefile,name='encrypt'),
    path('download/',User.views.download,name='download'),
    path('decrypt/<id>',User.views.decryptfile,name='viewdblock'),
    path('down/',User.views.down,name='down'),
    path('userh/',User.views.userhome,name='userh'),
    path('login/', visitor.views.login, name='login'),
    path('payment/', User.views.payment, name='payment'),
    path('paymentcon/',User.views.paymentcon,name='paymentcon'),
    path('savepayment/', User.views.savepayment, name='savepayment'),

]