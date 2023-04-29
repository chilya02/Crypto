from django.contrib.auth.models import AnonymousUser
from django.http import JsonResponse, HttpResponseRedirect


def is_auth(method: str):
    def auth_decorator(function):
        def _wrapper(request, *args, **kwargs):
            if not request.user == AnonymousUser():
                result = function(request, *args, **kwargs)
                if method == 'JSON':
                    result['balance'] = request.user.balance
                return result
            else:
                if method == 'JSON':
                    return JsonResponse({'redirect': '/uesrs/auth'})
                elif method == 'HTTP':
                    return HttpResponseRedirect('/users/auth')
        return _wrapper
    return auth_decorator


def balance(function):
    def _wrapper(request, *args, **kwargs):
        if not request.user == AnonymousUser():
            result = function(request, *args, **kwargs)
            result['balance'] = request.user.balance
            return result
    return _wrapper
