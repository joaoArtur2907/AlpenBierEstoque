# catalog/middleware.py
import threading

_thread_locals = threading.local()

def get_current_user():
    """Retorna o usuário logado na thread atual"""
    return getattr(_thread_locals, 'user', None)


class CurrentUserMiddleware:
    """
    Middleware captura usuario logado na requisicao para ser usado em outros lugares.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Guarda o usuário na memória local
        _thread_locals.user = getattr(request, 'user', None)

        response = self.get_response(request)

        # Limpa a memória para a próxima requisição
        if hasattr(_thread_locals, 'user'):
            del _thread_locals.user

        return response