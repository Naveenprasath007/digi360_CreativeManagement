from django import forms
from django.contrib.auth import authenticate,get_user_model

class UserLoginForm(forms.Form):
    username=forms.CharField()
    password=forms.CharField(widget=forms.PasswordInput)

    def clean(self,*args,**kwargs):
        username=self.cleaned_data.get('username')
        password=self.cleaned_data.get('password')

        if username and password:
            user=authenticate(username=username,password=password)

            if not user:
                raise forms.ValidationError('User Does Not Exist')
            
            if not user.check_password(password):
                raise forms.ValidationError('Incorrect Password')
        
        return super(UserLoginForm, self).clean(*args,**kwargs)

user=get_user_model()

class UserRegisterForm(forms.ModelForm):
    ROLE_CHOICES= [
    ('Creator', 'Creator'),
    ('Approver', 'Approver'),
    ('Downloader', 'Downloader'),
    ]

    # email=forms.EmailField(label='Email Address')
    # email2=forms.EmailField(label='Confirm Email Address')
    username=forms.CharField(label=False,widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    email=forms.EmailField(label=False,widget=forms.TextInput(attrs={'placeholder': 'Email Address'}))
    Name=forms.CharField(label=False,widget=forms.TextInput(attrs={'placeholder': 'Enter Your Name'}))
    Role=forms.CharField(label=False, widget=forms.Select(choices=ROLE_CHOICES))
    password=forms.CharField(label=False,widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

    class Meta:
        model=user
        fields=[
            'Name',
            'email',
            'username',
            # 'email2',
            'password',
            'Role',
        ]

    def clean(self,*args,**kwargs):
        email=self.cleaned_data.get('email').lower()
        # email2=self.cleaned_data.get('email2')

        # if email!=email2:
        #     raise forms.ValidationError("Emails Don't Match")

        email_qs=user.objects.filter(email=email)
        if email_qs.exists():
            raise forms.ValidationError("Emails Already In Use")

        return super(UserRegisterForm, self).clean(*args,**kwargs)
        

  
class ActivationForm(forms.Form):
    ROLE_CHOICES= [
    ('U1', 'Creator'),
    ('R1', 'Approver'),
    ('D1', 'Downloader'),
    ]
    email = forms.CharField()
    Role=forms.CharField(label='Select Role', widget=forms.Select(choices=ROLE_CHOICES)) 