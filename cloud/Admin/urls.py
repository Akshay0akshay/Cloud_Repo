from django.urls import path
import Admin.views
urlpatterns = [

    path('approveuser/',Admin.views.viewuser,name='approveuser'),
    path('approve/<id>',Admin.views.approve,name='approve'),
    path('reject/<id>',Admin.views.reject,name='reject'),
    path('approvefile/', Admin.views.viewfile,name='approvefile'),
    path('viewblock/<id>',Admin.views.viewefile,name='viewblock'),
    path('verify/',Admin.views.verify,name='verify'),
    path('banking/', Admin.views.banking, name='banking'),
    path('addbank/', Admin.views.addbank, name='bank'),
    path('addbranch/', Admin.views.addbranch, name='branch'),
    path('addaccount/', Admin.views.addaccount, name='account'),
    path('brnch/', Admin.views.brnch, name='brnch'),
    path('viewpayment/',Admin.views.viewpayment,name='viewpayment')


]