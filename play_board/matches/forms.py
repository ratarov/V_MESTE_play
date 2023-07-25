from django import forms
from django.utils import timezone

from users.models import User
from games.models import Game

from .models import Player, Match


class PlayerForm(forms.ModelForm):
    name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-sm',
            'placeholder': 'Имя игрока',
        })
    )
    user = forms.ModelChoiceField(
        queryset=User.objects.none(),
        required=False,
    )
    username = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-sm',
            'list': 'users',
            'placeholder': 'Введите username',
        }),
    )
    team = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-sm',
            'placeholder': 'Цвет/название',
        }),
    )
    score = forms.IntegerField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-sm',
        }),
    )

    class Meta:
        model = Player
        fields = ('name', 'user', 'username', 'team', 'score', 'winner')

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name:
            raise forms.ValidationError('Имя - обязательное поле')
        return name

    def clean_user(self):
        user = None
        if self.data.get('username'):
            user = User.objects.filter(
                username=self.data.get('username')).first()
            if not user:
                raise forms.ValidationError('Нет такого пользователя')
        return user


class MatchForm(forms.ModelForm):

    date = forms.DateField(
        initial=timezone.now(),
        widget=forms.DateInput(
            format=('%Y-%m-%d'),
            attrs={'class': 'form-control form-control-sm', 'type': 'date'}
        )
    )
    game = forms.ModelChoiceField(
        queryset=Game.objects.all(),
        widget=forms.Select(attrs={
            'class': 'game-select', 'style': 'width: 100%;'
        })
    )
    status = forms.CharField(required=False)

    class Meta:
        model = Match
        fields = ('date', 'game', 'place', 'type', 'quantity', 'length',
                  'comments', 'ignore', 'incomplete', 'status')
        widgets = {'comments': forms.Textarea(attrs={
            'rows': '3', 'class': 'form-control',
        })}

    def __init__(self, *args, **kwargs):
        super(MatchForm, self).__init__(*args, **kwargs)
        self.fields['place'] = forms.ChoiceField(choices=self.get_places())

    def get_places(self):
        places = list(
            self.instance.creator.places.values_list('name', flat=True)
        )
        default = [
            ('квартира/дом', 'квартира/дом'),
            ('клуб/антикафе', 'клуб/антикафе'),
            ('кафе/бар', 'кафе/бар'),
            ('мероприятие', 'мероприятие'),
        ]
        return [(place, place) for place in places] + default

    def clean_status(self):
        if self.cleaned_data.get('ignore'):
            return Match.Status.IGNORE
        return Match.Status.OK


class UserMatchesForm(forms.ModelForm):
    status_options = [('', 'Не важно')] + Match.Status.choices
    status = forms.ChoiceField(choices=status_options, required=False)
    game = forms.ModelChoiceField(
        queryset=Game.objects.all(),
        required=False,
        widget=forms.Select(attrs={
            'class': 'game-select', 'style': 'width: 100%;'
        })
    )
    date_since = forms.DateField(
        required=False, widget=forms.DateInput(
            format=('%Y-%m-%d'),
            attrs={'class': 'form-control', 'type': 'date'}
        )
    )
    date_until = forms.DateField(
        required=False,
        widget=forms.DateInput(
            format=('%Y-%m-%d'),
            attrs={'class': 'form-control', 'type': 'date'}
        )
    )

    class Meta:
        model = Match
        fields = ('status', 'game', 'date_since', 'date_until')
