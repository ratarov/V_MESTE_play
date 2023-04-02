from meetings.models import Meeting
from django.utils import timezone


def update_meeting_status():
    """Обновление статуса встреч на завершенные"""
    meetings = Meeting.objects.filter(
        start_date__lt=timezone.now(), status_id=1
    )
    updated_meetings = []
    for meeting in meetings:
        meeting.status_id = 2
        updated_meetings.append(meeting)
    Meeting.objects.bulk_update(updated_meetings, ['status'])
    print('Регулярное обновление статуса встреч')
