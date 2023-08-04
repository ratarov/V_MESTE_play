from django import forms
from django.db.models import Q
from django.utils import timezone

from users.models import User, Place
from games.models import Game

from .models import Player, Match


class PlayerForm(forms.ModelForm):
    """Форма для заполнения данных игрока в партии."""
    name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Имя игрока',
        }),
    )
    user = forms.ModelChoiceField(
        queryset=User.objects.none(),
        required=False,
    )
    username = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'list': 'users',
            'placeholder': 'Введите username',
        }),
    )
    team = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Цвет/название',
        }),
    )
    score = forms.IntegerField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        }),
    )

    class Meta:
        model = Player
        fields = ('name', 'user', 'username', 'team', 'score', 'winner')

    def clean_user(self):
        user = None
        if self.data.get('username'):
            user = User.objects.filter(
                username=self.data.get('username')).first()
            if not user:
                raise forms.ValidationError('Нет такого пользователя')
        return user

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name:
            raise forms.ValidationError('Имя - обязательное поле')
        return name


class MatchForm(forms.ModelForm):
    """Форма для заполнения параметров партии"""
    date = forms.DateField(
        initial=timezone.now(),
        widget=forms.DateInput(
            format=('%Y-%m-%d'),
            attrs={'class': 'form-control', 'type': 'date'}
        )
    )
    game = forms.ModelChoiceField(
        queryset=Game.objects.all(),
        widget=forms.Select(attrs={
            'class': 'game-select', 'style': 'width: 100%;'
        })
    )
    status = forms.CharField(required=False)
    place = forms.ModelChoiceField(queryset=None, required=False)

    class Meta:
        model = Match
        fields = ('date', 'game', 'place', 'type', 'quantity', 'length',
                  'comments', 'ignore', 'incomplete', 'status')
        widgets = {'comments': forms.Textarea(attrs={
            'rows': '3', 'class': 'form-control',
        })}

    def __init__(self, *args, **kwargs):
        super(MatchForm, self).__init__(*args, **kwargs)
        match_creator = self.instance.creator
        self.fields['place'].queryset = Place.objects.filter(
            Q(creator=match_creator) | Q(matches__creator=match_creator)
        ).distinct()

    def clean_status(self):
        if self.cleaned_data.get('ignore'):
            return Match.Status.IGNORE
        return Match.Status.OK


class UserMatchesForm(forms.ModelForm):
    """Форма для фильтра списка матчей."""
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


class StatFilterForm(forms.Form):
    """Форма для фильтра статистики матчей."""
    empty = [('', '---------')]
    game = forms.ModelChoiceField(
        queryset=None,
        required=False,
        widget=forms.Select(attrs={
            'class': 'game-select', 'style': 'width: 100%;'
        })
    )
    date_since = forms.DateField(
        required=False,
        initial=timezone.now() - timezone.timedelta(days=90),
        widget=forms.DateInput(
            format=('%Y-%m-%d'),
            attrs={'class': 'form-control', 'type': 'date'}
        )
    )
    date_until = forms.DateField(
        required=False,
        initial=timezone.now(),
        widget=forms.DateInput(
            format=('%Y-%m-%d'),
            attrs={'class': 'form-control', 'type': 'date'}
        )
    )
    place = forms.ModelChoiceField(queryset=None, required=False)
    type = forms.ChoiceField(
        choices=empty + Match.Type.choices,
        required=False,
    )
    player = forms.ModelChoiceField(queryset=None, required=False)

    class Meta:
        model = Match
        fields = ('game', 'date_since', 'date_until',
                  'place', 'type', 'player')

    def __init__(self, user, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields['player'].queryset = (
            User.objects.
            filter(played__match__players__user=user).
            distinct().
            order_by('username')
        )
        self.fields['place'].queryset = (
            Place.objects.filter(matches__players__user=user).distinct()
        )
        self.fields['game'].queryset = (
            Game.objects.filter(matches__players__user=user).distinct()
        )
