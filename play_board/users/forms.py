from django import forms
from django.contrib.auth.forms import UserCreationForm
from meetings.models import Meeting
from users.models import Place, User


class PlaceForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = ('type', 'name', 'city', 'address', 'building', 'flat',
                  'comments')
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


class UserMeetingsForm(forms.ModelForm):
    status_options = (
        ('', 'Не важно'),
        ('Готовится', 'Готовится'),
        ('Отменена', 'Отменена'),
        ('Прошла', 'Прошла'),
    )
    host_options = (
        ('', 'Не важно'),
        ('Вы', 'Вы'),
        ('Кто-то другой', 'Кто-то другой'),
    )
    status = forms.ChoiceField(choices=status_options, required=False)
    host = forms.ChoiceField(choices=host_options, required=False)
    date_since = forms.DateField(
        required=False, widget=forms.DateInput(
            format=('%Y-%m-%d'),
            attrs={'class': 'form-control form-control-sm', 'type': 'date'}
        )
    )
    date_until = forms.DateField(
        required=False,
        widget=forms.DateInput(
            format=('%Y-%m-%d'),
            attrs={'class': 'form-control form-control-sm', 'type': 'date'}
        )
    )

    class Meta:
        model = Meeting
        fields = ('status', 'host', 'date_since', 'date_until')
