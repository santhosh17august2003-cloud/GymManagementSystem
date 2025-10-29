from django.contrib import admin
from django.urls import path
from gym import views 
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static    
from django.contrib.auth.views import LogoutView  

urlpatterns = [
    path('', views.log, name='home'),  
    path('admin/', admin.site.urls),  
    path("Home", views.Home, name="Home"),
    path('register', views.register, name="register"),
    path('log', views.log, name="log"),
    path('payment', views.payment, name="payment"),
    path('adpayment', views.adpayment, name="adpayment"),
    path('sixpayment', views.sixpayment, name="sixpayment"),
    path('pay', views.pay, name="pay"),
    path('one', views.one, name="one"),
    path("onepayment/", views.onepayment, name="onepayment"),
    path('attendanceview', views.attendanceview, name="attendanceview"),
    path("add_product", views.add_product, name="add_product"),
    path('products', views.product_list, name='product_list'),
    path('updatethree/<int:id>', views.updatethree, name="updatethree"),
    path('three-month/', views.render_three_month_payment_view, name='render_three_month_payment_view'),
    path('updatesix/<int:id>/', views.updatesix, name='updatesix'),
    path('six-month/', views.render_six_month_payment_view, name='render_six_month_payment_view'),
    path('updateyear/<int:id>/', views.updateyear, name='updateyear'),
    path('one-year/', views.render_one_year_payment_view, name='render_one_year_payment_view'),
    path('logout', views.log, name='log'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
