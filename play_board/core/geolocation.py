import logging

from geopy.geocoders import Nominatim

logger = logging.getLogger(__name__)


def get_geolocation(location):
    """Получение геопозиции по адресу"""
    try:
        geolocator = Nominatim(user_agent="Tester")
        geolocation = geolocator.geocode(location)
        return geolocation
    except Exception:
        logger.error('Ошибка доступа к сервису геолокации')
    return None
