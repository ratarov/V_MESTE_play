class EndpointError(Exception):
    """Эндпоинт не возвращает ожидаемый ответ 200."""
    pass


class TimeoutError(Exception):
    """Истекло время ожидания ответа с эндпоинта."""
    pass
