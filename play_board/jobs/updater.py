from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from .jobs import update_meeting_status


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_meeting_status, 'interval', hours=8)
    scheduler.start()
    