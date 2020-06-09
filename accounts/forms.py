from django.forms.models import model_to_dict, fields_for_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from django import forms
from .models import UserProfile
User = get_user_model()


class UserForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__icontains=email).exists():
            raise forms.ValidationError('This email is already taken')
        return email

    class Meta:
        model = User
        fields = ['first_name', 'last_name',  'username',
                  'email', 'password1', 'password2']


class ProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ['bio', 'image']

        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control mb-2'}),
            'image': forms.FileInput(attrs={'class': 'form-control mb-2'}),
            'social': forms.Textarea(attrs={'class': 'form-control mb-2'}),
        }


class UserDetailsForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name',
                  'email', ]
