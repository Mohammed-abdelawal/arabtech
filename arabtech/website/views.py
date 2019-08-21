# basic views imports
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
#renders and authenticate imports
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.decorators import login_required
#local forms and models imports
from django.shortcuts import render, get_object_or_404
from .forms import EditUserForm, ProfileForm, ServiceForm, UserForm, InvoiceItemForm
from .models import User, Product, Partner, Profile, Category, Cart, Wishlist, Invoice, InvoiceItem
#ajax imports
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
#==========================================================================
""" Here i will define views that user can login, logout, register with """
#==========================================================================

def registerPage(request):
    """ this view is to register new user """
    if request.method == 'POST':
        userForm =  UserForm(request.POST )
        profileForm =  ProfileForm(request.POST ,request.FILES )

        if userForm.is_valid() and profileForm.is_valid():
            user = userForm.save()
            profile = profileForm.save(False)
            profile.user_id = user
            if 'pic' in request.FILES:
                profile.pic = request.FILES['pic']
            profile.save() 
            login(request,user)
            return HttpResponseRedirect(reverse('home'))
        else:
            print(userForm.errors)
            print(profileForm.errors)
    else:
        userForm =  UserForm()
        profileForm =  ProfileForm()

    return render(request, 'register.html', {
        'userForm':userForm,
        'profileForm':profileForm})
    
def loginPage(request):
    """ this view for login active user """
    if request.method == 'POST':
        userName =request.POST.get('username')
        password =request.POST.get('password')
        user = authenticate(username=userName,password=password)
        if user:
            login(request,user)
            return HttpResponseRedirect(reverse('home'))
        else:
            return HttpResponse('invalid user')
    else:
        return render(request,'login.html')

@login_required
def logoutPage(request):
    """ this page is to confirm logout """
    logout(request)
    return HttpResponseRedirect(reverse('home'))









#================================================================================================
""" let's define our views that show our Partners, Categories, Products List, Product Details """
#================================================================================================


def partnerPage(request,name=None):
    partnerObject = get_object_or_404(  Partner ,name = name)
    partnerProducts = Product.objects.filter(partner = partnerObject )
    partners = Partner.objects.filter()
    partner_name = []
    for i in partners:
        partner_name.append(i.name)
    category = Category.objects.all()
    cat_name = []
    for i in category:
        cat_name.append(i.name)
    return render(request,'partner.html',{'partnerObject':partnerObject,'partnerProducts':partnerProducts,'title':(name+' | ArabTech'),'category_name':cat_name,'partner_name':partner_name})


def partnerList(request):
    partners = Partner.objects.filter()
    partner_name = []
    for i in partners:
        partner_name.append(i.name)
    category =   Category.objects.all()
    cat_name = []
    for i in category:
        cat_name.append(i.name)
    return render(request,'partnerList.html',{'partners':partners,'title':' Partners | ArabTech','category_name':cat_name,'partner_name':partner_name})


def categoryPage(request,name=None):
    categoryObj = get_object_or_404(Category ,name = name)
    categoryProducts =   Product.objects.filter( category = categoryObj )
    category =   Category.objects.all()
    cat_name = []
    for i in category:
        cat_name.append(i.name)
    partner =   Partner.objects.all()
    partner_name = []
    for i in partner:
        partner_name.append(i.name)
    return render(request,'category.html',{'categoryObj':categoryObj,'categoryProducts':categoryProducts,'title':(name+' | ArabTech'),'category_name':cat_name,'partner_name':partner_name})



def productDetails(request,name='all'):
    product = get_object_or_404(  Product, name=name)
    
    category =   Category.objects.all()
    cat_name = []
    for i in category:
        cat_name.append(i.name)
    
    partner =   Partner.objects.all()
    partner_name = []
    for i in partner:
        partner_name.append(i.name)
    return render(request,'product.html',{'product':product,'title':(name+' | ArabTech'),'category_name':cat_name,'partner_name':partner_name})


def productsList(request):
    products_order_by_cat=[]
    category =   Category.objects.filter()
    cat_name=[]
    for cat in category :
        cat_name.append(cat.name)
        products =   Product.objects.filter(category = cat)
        cat_products = []
        for product in products :
            cat_products.append(product)
        products_order_by_cat.append(cat_products)

    partner =   Partner.objects.all()
    partner_name = []
    for i in partner:
        partner_name.append(i.name)
    return render(request,'productsList.html',{'productsList':products_order_by_cat,'title':'Products | ArabTech','category_name':cat_name,'partner_name':partner_name})
    

#======================================================================================
""" user views """
#======================================================================================

@login_required
def profilePage(request, username = None):
    if request.user.username != username :
        raise Http404('you can\'t see others profiles')
    if request.method == 'POST' :
        userModel = get_object_or_404(  User,username=username)
        profileModel = get_object_or_404(  Profile,user_id=userModel.pk)
        userForm =  EditUserForm(request.POST ,instance=userModel)
        profileForm =  ProfileForm(request.POST ,request.FILES,instance=profileModel )
        if userForm.is_valid() and profileForm.is_valid():
            user = userForm.save()
            profile = profileForm.save(False)
            profile.user_id = user
            if 'pic' in request.FILES:
                profile.pic = request.FILES['pic']
            profile.save()
        return HttpResponseRedirect('user/'+username)
    else:
        user = get_object_or_404(  User,username=username)
        profile = get_object_or_404(  Profile,user_id=user)
        userForm = EditUserForm(initial={'first_name':user.first_name,
            'last_name':user.last_name, 
            'email':user.email})
        profileForm = ProfileForm(initial={'pic':profile.pic, 
            'job':profile.job, 
            'organization':profile.organization, 
            'about':profile.about, 
            'phone':profile.phone, 
            'Gender':profile.Gender, 
            'birthdate':profile.birthdate, 
            'address':profile.address})

        wishlist = Wishlist.objects.filter(user=request.user)
        
        invoices = Invoice.objects.filter(client = request.user)

        category =   Category.objects.all()
        cat_name = []
        for i in category:
            cat_name.append(i.name)
        partner =   Partner.objects.all()
        partner_name = []
        for i in partner:
            partner_name.append(i.name)

        return render(request,'profile.html',{'title':'About | ArabTech',
            'category_name':cat_name,
            'partner_name':partner_name,
            'userForm':userForm,
            'profileForm':profileForm,
            'wishlist':wishlist,
            'invoices':invoices})





























































#=====================================================================================
"""  about company views  """
#=====================================================================================


def about(request):
    category =   Category.objects.all()
    cat_name = []
    for i in category:
        cat_name.append(i.name)
    partner =   Partner.objects.all()
    partner_name = []
    for i in partner:
        partner_name.append(i.name)
    return render(request,'about.html',{'title':'About | ArabTech','category_name':cat_name,'partner_name':partner_name})


def home(request):

    category =   Category.objects.all()
    cat_name = []
    for i in category:
        cat_name.append(i.name)
    
    partner =   Partner.objects.all()
    partner_name = []
    for i in partner:
        partner_name.append(i.name)

    return render(request,'index.html',{'title':'Home | ArabTech','category_name':cat_name,'partner_name':partner_name})


def services(request):
    if request.method == 'POST':
        serviceForm = ServiceForm(request.POST)
        if serviceForm.is_valid():
            service = serviceForm.save(False)
            service.user = request.user
            service.save()
            return HttpResponseRedirect(reverse('home'))
    serviceForm = ServiceForm()
    category = Category.objects.all()
    cat_name = []
    for i in category:
        cat_name.append(i.name)
    partner =   Partner.objects.all()
    partner_name = []
    for i in partner:
        partner_name.append(i.name)
    return render(request,'services.html',{'title':'Services | ArabTech','category_name':cat_name,'partner_name':partner_name,'serviceForm':serviceForm})


def admin_orders(request):
    if not request.user.is_staff :
        raise Http404('this is for staff only')
    else :
        pass



#---------------------------------------------------
""" ajax system """
#---------------------------------------------------
@login_required
def cart(request):
    cart = Cart.objects.filter(client=request.user)
    html = render_to_string('cart.html',{'cart':cart},request=request)
    return JsonResponse({'cart':html})

@login_required
def cart_item_delete(request, pk=None):
    get_object_or_404(Cart,id=pk).delete()
    cart = Cart.objects.filter(client=request.user)
    html = render_to_string('cart.html',{'cart':cart},request=request)
    return JsonResponse({'cart':html})

@login_required
def cart_delete(request):
    Cart.objects.filter(client=request.user).delete()
    return JsonResponse(dict())

@login_required
@csrf_exempt
def cart_add(request,product):
    if Cart.objects.filter(client=request.user,product = Product.objects.get(pk=product)):
        return JsonResponse({'respond':0})
    cart = Cart(client=request.user,product = Product.objects.get(pk=product))
    cart.save()
    return JsonResponse({'respond':1})

@login_required
def cart_order(request):
    cart = Cart.objects.filter(client=request.user)
    if cart :
        invoice = Invoice(client=request.user)
        invoice.save()
        for i in cart :
            invoice_item = InvoiceItem(product= i.product,invoice=invoice)
            invoice_item.save()
            i.delete()
        return JsonResponse({'respond':1})
    else :
        return JsonResponse({'respond':0})


@login_required
def wishlist_add(request,product):
    if Wishlist.objects.filter(user=request.user,product = Product.objects.get(pk=product) ):
        return JsonResponse({'respond':0})
    cart = Wishlist(user=request.user,product = Product.objects.get(pk=product))
    cart.save()
    return JsonResponse({'respond':1})

@login_required
def edit_invoice(request,pk):
    if request.method == 'POST':
        data_list = []
        print(request.POST)
        for key in request.POST:
            print(key)
            invoiceItemForm =  InvoiceItemForm(request.POST[key] ,instance=InvoiceItem.objects.get(product=serviceForm['product']))
            if serviceForm.is_valid():
                invoice_item = invoiceItemForm.save()
        return HttpResponseRedirect(reverse('home'))
    else:
        invoice_object = Invoice.objects.get(id=pk)
        invoice_item_object = InvoiceItem.objects.filter(invoice = pk)
        invoice_items = []
        for item in invoice_item_object :
            invoice_item_form = InvoiceItemForm(initial={'product':item.product,'quantity':item.quantity})
            invoice_items.append(invoice_item_form)
        html = render_to_string('editInvoice.html',{'invoice_items':invoice_items,'invoice':invoice_object})
        return JsonResponse({'invoice':html})






#|||||||||||||||||||||||||||||||||||||||||||||||||
#=================================================
#=================================================
#=================================================
#|||||||||||||||||||||||||||||||||||||||||||||||||









def testbase(request):

    category =   Category.objects.all()
    cat_name = []
    for i in category:
        cat_name.append(i.name)
    
    partner =   Partner.objects.all()
    partner_name = []
    for i in partner:
        partner_name.append(i.name)
    
    return render(request,'index.html',{'title':'base','category_name':cat_name,'partner_name':partner_name})















