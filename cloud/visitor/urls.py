from django.urls import path
import visitor.views

urlpatterns = [

    path('login/',visitor.views.login,name='login'),
    path('adminm/',visitor.views.admin,name='admin'),
    path('logout/', visitor.views.logout,name='logout'),
    path('reg/', visitor.views.reg,name='reg'),
    path('userhome/',visitor.views.umaster,name='umaster'),
    path('unamecheck/<uname>',visitor.views.unamecheck),
    path('',visitor.views.index,name='index')

]