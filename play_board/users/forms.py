from django import forms
from django.contrib.auth.forms import UserCreationForm
from users.models import Place, User


class PlaceForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = ('type', 'name', 'city', 'address', 'flat', 'comments')
        widgets = {'comments': forms.Textarea(attrs={
            'rows': '5', 'class': 'form-control',
        })}


class UserInfoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('photo', 'first_name', 'last_name', 'email',
                  'country', 'city', 'about', 'telegram', 'tesera_account',
                  'bgg_account')
        widgets = {'about': forms.Textarea(attrs={
            'rows': '5', 'class': 'form-control',
        })}

class CreateUserForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')
