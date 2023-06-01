from geopy.geocoders import Nominatim

from .exceptions import EndpointError


def get_geolocation(location):
    """Получение геопозиции по адресу"""
    try:
        geolocator = Nominatim(user_agent="Tester")
        geolocation = geolocator.geocode(location)
    except Exception:
        raise EndpointError('Ошибка доступа к сервису геолокации')
    return geolocation
