from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


from .models import Wishlist, Product, Service, Partner, Category, Profile, Invoice, InvoiceItem, Property, Cart, User

# Register your  here.

admin.site.register( Service)
admin.site.register( Partner)
admin.site.register( Category)
admin.site.register( Cart)


class InvoiceItem_inline(admin.TabularInline):
    model =  InvoiceItem
    extra =1

class InvoiceAdmin(admin.ModelAdmin): 
    inlines = [InvoiceItem_inline]
    list_display = ('id','__str__', 'record')
    list_filter = ['record','client']
    readonly_fields=('record', 'client')

admin.site.register( Invoice,InvoiceAdmin)

admin.site.register(Wishlist)


class Property_inline(admin.TabularInline):
    model =  Property
    extra =3

class ProductAdmin(admin.ModelAdmin): 
    inlines = [Property_inline]

admin.site.register( Product, ProductAdmin)





# custom user to add profile model

def not_staff(modeladmin, request, queryset):
    if request.user.is_superuser :
        queryset.update(
            is_staff = False
        )
not_staff.short_description = 'desactive staff'

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name = 'Profile'
    fk_name = 'user'
    radio_fields = {'Gender':admin.HORIZONTAL}


#('pic', 'user', 'job', 'organization', 'about', 'phone', 'is_Male', 'birthdate', 'address' )

class CustomUserAdmin(UserAdmin):
    inlines = [ProfileInline,]
    UserAdmin.actions += [not_staff]
    
    #UserAdmin.list_display += ('username',) 

admin.site.unregister(User)
admin.site.register(User,CustomUserAdmin)