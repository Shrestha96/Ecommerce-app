from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from scorptec.models import UserDetail
#imports for crispy form to render form
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Div, Submit, Reset, Field, HTML
#importing for form validation
from django.db import transaction
from scorptec.validators import validate_dob
#changing the type of DateInput from text to date
class DateInput(forms.DateInput):
    input_type = 'date'

#variable for gender choice
GENDER = [
    (None, '-------'),
    ('male','Male'),
    ('female','Female'),
]
#User model form to register account
class UserForm(forms.ModelForm):
    #additional attributes to show in form display
    password  = forms.CharField(widget = forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password'}))
    confirm_password =forms.CharField(help_text = "Confirm Your Password",widget = forms.PasswordInput(attrs={'class':'form-control','placeholder':' Confirm Password'}))
    verify_email =forms.EmailField(label='Email',widget = forms.EmailInput(attrs={'class':'form-control', 'placeholder': 'Confirm Email'}))

    class Meta():
        model = User #extending user model form
        fields = ('username','first_name' ,'last_name','email','password')

        widgets = {
            'username':forms.TextInput(attrs={'class':'form-control', 'placeholder': 'User Name'}),
            'first_name':forms.TextInput(attrs={'class':'form-control', 'placeholder': 'First Name'}),
            'last_name':forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Last Name'}),
            'email':forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Email Address'}),
        }

    def clean_username(self):
        username = self.cleaned_data['username']
        for instance in User.objects.all():
            if instance.username == username:
                raise ValidationError("Username already exist!!")
        return username




#getting additional information required
class UserDetailForm(forms.ModelForm):
    class Meta():
        model = UserDetail
        fields = ('gender','mobile','date_of_birth', 'address', 'zip_code','country')

        widgets ={
        'gender': forms.Select(choices=GENDER,attrs={'class':'form-control'}),
        'mobile': forms.NumberInput(attrs={'class':'form-control','placeholder':'Mobile Number'}),
        'date_of_birth': DateInput(attrs={'class':'form-control', 'placeholder':'Date of Birth'}),
        'address': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Address'}),
        'zip_code': forms.NumberInput(attrs={'class':'form-control','placeholder':'ZIP code'}),
        'country': forms.TextInput(attrs={'class':'form-control','placeholder':'Country'}),
        }


class CustomRegisterForm(forms.Form):
    username = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'User Name'}),
        max_length=50
    )
    first_name = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
        max_length=50
    )
    last_name = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
        max_length=50
    )
    email = forms.EmailField(
        label='',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'})
    )
    verify_email = forms.EmailField(
        label='',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Email'})
    )
    mobile = forms.IntegerField(
        label='',
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Mobile Number'})
    )
    gender = forms.ChoiceField(
        label='',
        choices=GENDER
    )
    password1 = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )
    password2 = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': ' Confirm Password'})
    )
    date_of_birth = forms.DateField(
        label='',
        validators=[validate_dob],
        widget=DateInput(attrs={'class': 'form-control', 'placeholder': 'Date of Birth'})
    )
    address = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address'}),
        max_length=250
    )
    zip_code = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ZIP Code'}),
        max_length=4
    )
    country = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country'}),
        max_length=15
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Field('username')
            ),
            Row(
                Column('first_name', css_class='form-group col-md-6 mb-0'),
                Column('last_name', css_class='form-group col-md-6 mb-0'),
                css_class='row mt-2'
            ),
            Row(
                Column('email', css_class='form-group col-md-6 mb-0'),
                Column('verify_email', css_class='form-group col-md-6 mb-0'),
                css_class='row mt-2'
            ),
            Row(
                Column('mobile', css_class='form-group col-md-6 mb-0'),
                Column(
                    Div(
                        Div(
                            HTML('<label> Gender <span class="asteriskField">*</span> </label>'),
                            css_class='col-md-4'
                        ),
                        Field('gender', wrapper_class='col-md-8'),
                        css_class='row align-items-center'
                    ),
                    css_class='form-group col-md-6 mb-0'
                ),
                css_class='row mt-2'
            ),
            Row(
                Column('password1', css_class='form-group col-md-6 mb-0'),
                Column('password2', css_class='form-group col-md-6 mb-0'),
                css_class='row mt-2'
            ),
            Row(
                Div(
                    HTML('<label> Date of Birth <span class="asteriskField">*</span> </label>'),
                    css_class='col-md-3'
                ),
                Column(Field('date_of_birth'), css_class='form-group col-md-9'),
                css_class='row mt-2 align-items-center'
            ),
            Field('address', css_class='mt-2'),
            Row(
                Column('zip_code', css_class='form-group col-md-6 mb-0'),
                Column('country', css_class='form-group col-md-6 mb-0'),
                css_class='row mt-2'
            ),
            Div(
                HTML(
                    '<input type="submit" name="submit" value="Register" class="btn btn-success">'
                ),
                HTML(
                    '<input type="reset" class="btn btn-danger mx-3">'
                ),
                css_class='mt-3 text-center'
            ),
        )

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username__icontains=username).exists():
            raise forms.ValidationError('Username is already taken')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email__icontains=email).exists():
            self.add_error('email', 'Email is already taken')
        return email

    def clean_gender(self):
        gender = self.cleaned_data['gender']
        if not gender:
            raise forms.ValidationError('Gender is required')
        return gender

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data['email']
        verify_email = cleaned_data['verify_email']
        if email != verify_email:
            raise forms.ValidationError('Email and Verification Email must be same')

        password1 = cleaned_data['password1']
        password2 = cleaned_data['password2']
        if password1 != password2:
            raise forms.ValidationError('Both passwords must be same')
        return cleaned_data

    class Meta:
        fields = (
            'username', 'first_name', 'last_name', 'email', 'verify_email', 'password1', 'password2',
            'gender', 'mobile', 'date_of_birth', 'address', 'zip_code', 'country'
        )

    def save(self):
        username = self.cleaned_data['username']
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']
        email = self.cleaned_data['email']
        mobile = self.cleaned_data['mobile']
        gender = self.cleaned_data['gender']
        password1 = self.cleaned_data['password1']
        date_of_birth = self.cleaned_data['date_of_birth']
        address = self.cleaned_data['address']
        zip_code = self.cleaned_data['zip_code']
        country = self.cleaned_data['country']
        with transaction.atomic():
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password1,
                first_name=first_name,
                last_name=last_name
            )
            user_detail = UserDetail.objects.create(
                user=user,
                gender=gender,
                mobile=mobile,
                date_of_birth=date_of_birth,
                address=address,
                zip_code=zip_code,
                country=country
            )
        return user_detail
#needs to be modified
#creating sign up form
"""
class SignUp(forms.Form):
    first_name = forms.CharField(label='Firstname',widget = forms.TextInput(attrs={'class':'form-control', 'placeholder': 'First Name'}))
    last_name = forms.CharField(label='Lastname',widget = forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Last Name'}))
    email = forms.EmailField(label='Email',widget = forms.EmailInput(attrs={'class':'form-control', 'placeholder': 'Email'}))
    verify_email =forms.EmailField(label='Email',widget = forms.EmailInput(attrs={'class':'form-control', 'placeholder': 'Confirm Email'}))
    password = forms.CharField(label ='Password',widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password'}))
    verify_password =forms.CharField(label ='Password',widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Verify Password'}))
    mobile = forms.CharField(label ='Mobile',widget=forms.NumberInput(attrs={'class':'form-control','placeholder':'Mobile Number'}))
    date_of_birth= forms.DateTimeField(input_formats = ['%d/%m/%y'], widget=DateInput(attrs={'class':'form-control', 'placeholder':'Date of Birth'}))
    gender = forms.CharField(label ='Gender' ,widget=forms.Select(choices=GENDER,attrs={'class':'form-control'}))
    address = forms.CharField(label='Address',widget = forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Address'}))
    zip_code = forms.CharField(label ='ZIP code',widget=forms.NumberInput(attrs={'class':'form-control','placeholder':'ZIP code'}))
    country = forms.CharField(label ='Country',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Country'}))

"""

"""
#creating login_form
class LogIn(forms.Form):
    email = forms.EmailField(label='Email',widget = forms.EmailInput(attrs={'class':'form-control', 'placeholder': 'Email'}))
    password = forms.CharField(label ='Password',widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password'}))
"""
