from django import forms
from meetings.models import Comment, Meeting, MeetingParticipation
from users.models import Place
from games.models import Game
from django.utils import timezone


class MeetingSearchForm(forms.ModelForm):
    radius_vars = (
        [100, 100],
        [50, 50],
        [20, 20],
        [10, 10],
        [5, 5]
    )
    location = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control form-control-sm'}
    ))
    radius = forms.ChoiceField(choices=radius_vars, required=False)
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
    game = forms.ModelChoiceField(
        queryset=Game.objects.all(),
        required=False,
        widget=forms.Select(attrs={
            'class': 'game-select', 'style': 'width: 100%;'
        })
    )

    class Meta:
        model = Meeting
        fields = ('location', 'radius', 'date_since', 'date_until', 'game')


class MeetingForm(forms.ModelForm):
    games = forms.ModelMultipleChoiceField(
        queryset=Game.objects.all(),
        widget=forms.SelectMultiple(
            attrs={'class': 'form-control game-select'}
        )
    )
    place = forms.ModelChoiceField(queryset=None)

    def __init__(self, user, *args, **kwargs):
        super(MeetingForm, self).__init__(*args, **kwargs)
        self.fields['place'].queryset = Place.objects.filter(creator=user)

    class Meta:
        model = Meeting
        fields = ('games', 'start_date', 'start_time', 'guests',
                  'max_players', 'description', 'price', 'place', 'name')
        widgets = {
            'start_date': forms.DateInput(format=('%Y-%m-%d'), attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'start_time': forms.TimeInput(attrs={
                'class': 'form-control',
                "type": "time",
                "value": "19:00"
            }),
            'description': forms.Textarea(attrs={'rows': '5'})
        }
        labels = {
            'games': 'Игры',
            'description': 'Информация'
        }

    def clean_start_date(self):
        data = self.cleaned_data['start_date']
        if data < timezone.now().date():
            raise forms.ValidationError(
                'Дата встречи меньше сегодняшнего дня')
        return data

    def clean_max_players(self):
        max_players = self.cleaned_data['max_players']
        if self.instance.get_total_players():
            total_players_qty = self.instance.get_total_players()
            old_guests_qty = self.initial.get('guests')
        else:
            total_players_qty = 1         # organizer
            old_guests_qty = 0
        new_guests_qty = int(self.data.get('guests'))
        new_total = total_players_qty - old_guests_qty + new_guests_qty
        if max_players < new_total:
            raise forms.ValidationError(
                f'Максимум игроков ({max_players}) меньше кол-ва '
                f'игроков с гостями({new_total})'
            )
        return max_players


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)

        widgets = {'text': forms.Textarea(attrs={
            'rows': '5', 'class': 'form-control',
        })}


class GuestForm(forms.ModelForm):
    class Meta:
        model = MeetingParticipation
        fields = ('guests',)

    def __init__(self, user, meeting, *args, **kwargs):
        super(GuestForm, self).__init__(*args, **kwargs)
        self.meeting = meeting
        if user.is_authenticated:
            self.other_participants = meeting.participants.\
                filter(status='ACT').exclude(player=user)

    def clean_guests(self):
        data = self.cleaned_data['guests']
        players_without_user = self.other_participants.count()
        guests = sum(self.other_participants.values_list('guests', flat=True))
        max_qty = self.meeting.max_players
        if players_without_user + guests + data >= max_qty:
            print('aaa')
            raise forms.ValidationError(
                'Нет мест для указанного количества гостей')
        return data
