from datetime import datetime

from django.utils import timezone


def get_local_datetime(_datetime: datetime) -> str:
    return datetime.strftime(timezone.localtime(_datetime), "%d-%m-%Y %H:%M:%S")
