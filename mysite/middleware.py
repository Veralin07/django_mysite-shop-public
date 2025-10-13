import time
from django.http import HttpResponseForbidden

class RateLimitMiddleware:
    """
    Пример middleware, ограничивающего частоту запросов по IP.
    Позволяет делать один запрос с одного IP не чаще чем раз в RATE_LIMIT_INTERVAL секунд.
    """

    RATE_LIMIT_INTERVAL = 2  # секунда между запросами
    last_request_time_by_ip = {}

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = self.get_client_ip(request)
        now = time.time()

        # Исключаем пути документации из ограничения
        if request.path.startswith('/api/schema/') or request.path.startswith('/api/schema/swagger/') or request.path.startswith('/api/schema/redoc/'):
            return self.get_response(request)

        last_time = self.last_request_time_by_ip.get(ip)
        if last_time is not None:
            elapsed = now - last_time
            if elapsed < self.RATE_LIMIT_INTERVAL:
                # Если запрос пришел слишком быстро — блокируем
                return HttpResponseForbidden("Слишком частые запросы. Попробуйте позже.")

        # Запоминаем время запроса
        self.last_request_time_by_ip[ip] = now

        # Продолжаем обработку запроса дальше
        response = self.get_response(request)
        return response

    @staticmethod
    def get_client_ip(request):
        # Попытка получить IP пользователя
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
