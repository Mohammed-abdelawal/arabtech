from django.contrib import admin
from django.urls import path

from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.conf import settings
from django.conf.urls.static import static

from website import views

urlpatterns = [ 
    path('home', views.home ,name='home'),
    path('admin/', admin.site.urls),
    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage , name='login'),
    path('logout/', views.logoutPage ,name='logout'),

    path('product/all', views.productsList ,name='productall'),
    path('product/<str:name>', views.productDetails ,name='product'),
    path('category/<str:name>', views.categoryPage ,name='category'),
    path('partner/all', views.partnerList ,name='partnerall'),
    path('partner/<str:name>', views.partnerPage ,name='partner'),
    path('user/<str:username>', views.profilePage  ,  name='profile'),

    path('cart/', views.cart , name='cart'),
    path('cart/deleteitem/<int:pk>', views.cart_item_delete , name='cart_item_delete'),
    path('cart/delete', views.cart_delete , name='cart_delete'),
    path('cart/additem/<int:product>',views.cart_add , name='cart_add'),
    path('cart/order/', views.cart_order , name='cart_order'),
    path('wishlist/additem/<int:product>',views.wishlist_add,name='wishlist'),
    path('user/invoice/<int:pk>',   views.edit_invoice , name='invoice'),
    path('contact/',   views.testbase , name='contact'),
    path('team/', views.testbase , name='team'),
    path('about/', views.about , name='about'),
    path('service/', views.services , name='services'),
    path('user/orders/', views.testbase , name='invoices'),
]




""" override errors views """

#handler404 = 'website.views.my_custom_page_not_found_view'

#handler500 = 'mysite.views.my_custom_error_view'

#handler403 = 'mysite.views.my_custom_permission_denied_view'

#handler400 = 'mysite.views.my_custom_bad_request_view'




""" show your media files """ 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL , document_root=settings.MEDIA_ROOT)
