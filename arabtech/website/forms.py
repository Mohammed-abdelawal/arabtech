from django import forms
from .models import User, Profile, Service, InvoiceItem

# Create your forms here.

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name','last_name','username', 'email', 'password')

class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name','last_name', 'email')


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('pic', 'job', 'organization', 'about', 'phone', 'Gender', 'birthdate', 'address' )


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ( 'title', 'service_type', 'description', 'equipment')

class InvoiceItemForm(forms.ModelForm):
    delete = forms.BooleanField(required=False,initial=False)

    def __init__(self, *args, **kwargs):
        super(InvoiceItemForm, self).__init__(*args, **kwargs)
        if self.instance.id:
            self.fields['product'].widget.attrs['readonly'] = True

    def save(self, commit=True):
        if self.cleaned_data['delete']:
            return self.instance.delete()
        return super(InvoiceItemForm, self).save()
    
    class Meta:
        model = InvoiceItem 
        fields = ('product', 'quantity')
        readonly_fields = ('product',)
        


