from django.db import models

from django.core.exceptions import ValidationError

from django.core.validators import MaxValueValidator, MinValueValidator

from datetime import datetime

from django.contrib.auth.models import User
# Create your models here.


def validate_date(date):
    if date < datetime.now().date():
        raise ValidationError("Date cannot be in the past")






class Profile(models.Model):
    """Model definition for Profile."""

    # TODO: Define fields here

    pic = models.ImageField(
        upload_to = 'Person/',
        default = '',
        verbose_name = 'Profile pic',
        null = True,
        blank = True
        )

    user = models.OneToOneField(to=User,on_delete=models.CASCADE)
    job = models.CharField(verbose_name='Job title', max_length=250)
    organization = models.CharField(verbose_name='Organization', max_length=250)
    about = models.TextField(null=True, blank=True)
    phone = models.CharField(max_length=200, 
        help_text='you can add more than one number by Separate with \'-\' ')
    is_male = models.BooleanField(name='Gender',choices=((False,'Male') , (True,'Female')) )
    birthdate = models.DateField()
    address = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        """Meta definition for Profile."""

        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

    def __str__(self):
        """Unicode representation of Profile."""
        return (self.user_id.__str__() + ' - ' + self.job)



class Partner(models.Model):
    """Model definition for Partner."""

    # TODO: Define fields here

    name = models.CharField(max_length=255,unique=True)
    site = models.URLField(verbose_name='Website', help_text='put Partner website link here like : https://www.partner.com')
    desc = models.TextField(verbose_name='About Partner')
    logo = models.ImageField(upload_to='partner/',verbose_name=('Partner Logo'))
    field = models.CharField(max_length=200, verbose_name='Partner Field')

    class Meta:
        """Meta definition for Partner."""

        verbose_name = 'Partner'
        verbose_name_plural = 'Partners'

    def __str__(self):
        """Unicode representation of Partner."""
        return self.name +' - '+ self.pk.__str__()


class Category(models.Model):
    """Model definition for Category."""

    # TODO: Define fields here

    name = models.CharField(max_length=255,unique=True)
    desc = models.TextField(verbose_name='Description')

    class Meta:
        """Meta definition for Category."""

        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        """Unicode representation of Category."""
        return self.name



class Product(models.Model):
    """Model definition for Product."""

    # TODO: Define fields here

    name = models.CharField(max_length=255,unique=True)
    pic1 = models.ImageField(upload_to='product/',verbose_name='Primary Product Image')
    pic2 = models.ImageField(upload_to='product/',verbose_name='secondary Product Image', null=True, blank=True)
    price = models.FloatField(help_text='this price in EGP')
    desc = models.TextField(verbose_name='About Product')
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE)
    partner = models.ForeignKey(Partner,on_delete=models.CASCADE,null=True, blank=True)
    video = models.URLField(
        help_text='you should upload your video to youtube and provide the link here',
        null=True, 
        blank=True)

    discount = models.IntegerField(validators=[
            MaxValueValidator(100),
            MinValueValidator(0)],
             help_text='this is discount in precent', 
             verbose_name='discount precentage',
             default=0 )

    discount_exp_date = models.DateField(
        help_text='this date is about when to end the discount',
        null=True, 
        blank=True,
        validators=[validate_date]
        )

    class Meta:
        """Meta definition for Product."""

        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        """Unicode representation of Product."""
        return self.name




class Wishlist(models.Model):
    """Model definition for wishlist."""

    # TODO: Define fields here

    product = models.ForeignKey('Product',on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    class Meta:
        """Meta definition for wishlist."""

        verbose_name = 'Wishlist'
        
        unique_together = [['user', 'product']]

    def __str__(self):
        """Unicode representation of wishlist."""
        return str(self.product)+'  '+str(self.user)



class Invoice(models.Model):
    """Model definition for invoice."""

    # TODO: Define fields here

    client = models.ForeignKey(to=User, on_delete=models.CASCADE)
    record = models.DateTimeField(default=datetime.now, editable= False)
    in_progress = models.BooleanField(default=False)
    done = models.BooleanField(default=False)

    class Meta:
        """Meta definition for invoice."""
        verbose_name = 'invoice'
        verbose_name_plural = 'invoices'
        ordering = ['record']

    def get_status(self):
        if self.done :
            return 'Done'
        elif self.in_progress :
            return 'Progress'
        else :
            return 'Not Order'

    def __str__(self):
        """Unicode representation of invoice."""
        return str(self.pk) +' - '+User.objects.get_by_natural_key(self.client).username

#User.objects.get_by_natural_key(self.client).username -- work


class InvoiceItem(models.Model):
    """Model definition for InvoiceItem."""

    # TODO: Define fields here

    product = models.ForeignKey('Product',on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1,validators=[MinValueValidator(0),])
    invoice = models.ForeignKey('Invoice', on_delete=models.CASCADE)

    class Meta:
        """Meta definition for InvoiceItem."""

        verbose_name = 'InvoiceItem'
        verbose_name_plural = 'InvoiceItems'
        unique_together = [['invoice', 'product']]


class Service(models.Model):
    """Model definition for Order."""

    # TODO: Define fields here

    user = models.ForeignKey(User, on_delete = models.CASCADE)
    title = models.CharField(max_length=200)
    record = models.DateTimeField(auto_now_add=True)
    service_type = models.IntegerField(
        verbose_name='Service Type',
        choices=(
            (0,'Repair & Maintenance'),
            (1,'Consultation'),
            (2,'Installation of medical devices'),
            (3,'preparation of operating rooms and leisure'),
            (4,'preparation Intensive care rooms ( ICU & CCU)'),
            (5,'preparation of infant nursery centers'),
            (6,'Construction of gas networks for hospitals'),
            (7,'After-sales service'),
            (8,'Preparation of Radiology Centers'),
            (9,'Equipment outpatient clinics')
        )
    )
    description = models.TextField(verbose_name='about this service',null=True,blank=True)
    equipment = models.CharField(max_length=250,help_text='Device name')
    done = models.BooleanField(default=False)

    class Meta:
        """Meta definition for Service."""

        verbose_name = 'Service'
        verbose_name_plural = 'Services'
        ordering = ['record']
    def __str__(self):
        """Unicode representation of Service."""
        return self.title


class Property(models.Model):
    """Model definition for Properties."""

    # TODO: Define fields here
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    property_value = models.CharField(max_length=250)

    class Meta:
        """Meta definition for Property."""
        
        verbose_name = 'Property'
        verbose_name_plural = 'Propertiess'
        unique_together = [['name', 'product']]
    def __str__(self):
        """Unicode representation of Property."""
        return self.name



class Cart(models.Model):
    """Model definition for cart."""

    # TODO: Define fields here

    client = models.ForeignKey(to=User, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)

    class Meta:
        """Meta definition for cart."""

        verbose_name = 'cart'
        verbose_name_plural = 'carts'

        unique_together = [['client','product']]

    def __str__(self):
        """Unicode representation of cart."""
        return str(self.pk) +' - '+User.objects.get_by_natural_key(self.client).username


