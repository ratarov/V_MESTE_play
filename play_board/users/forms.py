from django import forms
from django.contrib.auth.forms import UserCreationForm

from core.geolocation import get_geolocation
from games.models import Game
from meetings.models import Meeting

from .models import BotConfig, Place, User


class PlaceForm(forms.ModelForm):
    loc_lat = forms.FloatField(required=False, disabled=True)
    loc_lon = forms.FloatField(required=False, disabled=True)

    class Meta:
        model = Place
        fields = ('type', 'name', 'city', 'address', 'building', 'flat',
                  'comments', 'loc_lat', 'loc_lon')
        widgets = {'comments': forms.Textarea(attrs={
            'rows': '5', 'class': 'form-control',
        })}

    def clean(self):
        cleaned_data = super().clean()
        city = cleaned_data['city']
        address = cleaned_data['address']
        building = cleaned_data['building']
        try:
            location = get_geolocation(f'{city}, {address} {building}')
            cleaned_data['loc_lat'] = location.latitude
            cleaned_data['loc_lon'] = location.longitude
        except AttributeError:
            raise forms.ValidationError(
                'Адрес не найден, попробуйте другой. '
                'Например, не сокращайте улицы: "пр." и "ул.".'
            )


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
        fields = ('username', 'email')


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


class BotConfigForm(forms.ModelForm):
    games = forms.ModelMultipleChoiceField(
        required=False,
        queryset=Game.objects.all(),
        widget=forms.SelectMultiple(
            attrs={'class': 'form-control game-select'}
        )
    )

    class Meta:
        model = BotConfig
        fields = ('is_active', 'comments_info', 'cancel_meeting_info',
                  'new_meeting_info', 'address', 'radius', 'games')

    # def clean_games(self):
    #     if all([self.cleaned_data['is_active'],
    #             self.cleaned_data['new_meeting_info'],
    #             not self.cleaned_data['games']]):
    #         raise forms.ValidationError(
    #             'Выберите хотя бы 1 игру для отслеживания новых встреч'
    #         )
    #     return self.cleaned_data['games']

    def clean_address(self):
        if all([self.cleaned_data['is_active'],
                self.cleaned_data['new_meeting_info'],
                not self.cleaned_data['address']]):
            raise forms.ValidationError(
                'Укажите адрес для отслеживания новых встреч'
            )
        return self.cleaned_data['address']
