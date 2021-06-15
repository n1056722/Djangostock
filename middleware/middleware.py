import hmac

from django.http import JsonResponse, HttpResponse
from django.utils.deprecation import MiddlewareMixin
from rest_framework import status

from appuser.models import AppUser, AppUserLog


class TokenCheckMiddleware(MiddlewareMixin):
    """
    使用中間建判斷打來的token是哪個使用者
    """

    def process_request(self, request):
        if request.path.startswith('/item/api/'):
            token = request.META.get('HTTP_X_STOCK_TOKEN')
            print(request.META)
            if token:
                try:
                    app_user = AppUser.objects.filter(token=token, is_enable=True).first()
                    request.app_user = app_user
                except Exception as e:
                    data = {
                        'msg': 'token error',
                    }
                    print(str(e))
                    return JsonResponse(status=status.HTTP_401_UNAUTHORIZED, data=data)
            else:
                data = {
                    'msg': 'token error',
                }
                return JsonResponse(status=status.HTTP_401_UNAUTHORIZED, data=data)


class SignatureCheckMiddleware(MiddlewareMixin):
    """
    確認傳過來的簽章是否有被竄改
    """

    def process_request(self, request):
        if request.path.startswith('/item/api/'):
            request_signature = request.META.get('HTTP_X_STOCK_SIGNATURE')
            # print(request.META)
            # try:
            app_user = request.app_user
            secret_key = app_user.secret_key
            print(secret_key)
            method = request.method
            path = request.path
            print(method, path)
            get_dict = dict(request.GET)  # {'uts': ['1622453552']} 取得uts裝進字典 1970
            sorted_get_dict = {k: v[0] for k, v in sorted(get_dict.items())}  # {'uts': '1622454017'}
            sorted_get_dict_string = "&".join(f"{k}={v}" for k, v in sorted_get_dict.items())  # uts=1622454289
            params = sorted_get_dict_string
            payload = method + path + params
            new_signature = hmac.new(secret_key.encode(), payload.encode(), 'sha256').hexdigest()
            if new_signature != request_signature:
                print(new_signature)
                print(request_signature)
                data = {
                    'msg': 'signature'
                }
                return JsonResponse(status=status.HTTP_401_UNAUTHORIZED, data=data)
            # except Exception as e:
            # data = {
            #     'status': 404,
            # }
            # print(str(e))
            # return JsonResponse(data=data)


class VisitTimesMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        if request.path.startswith('/item/api/'):
            try:
                if 200 <= response.status_code <= 299:
                    path = request.path
                    app_user = request.app_user
                    app_user_log = AppUserLog()
                    app_user_log.path = path
                    app_user_log.app_user = app_user
                    app_user_log.save()
            except Exception as e:
                print(str(e))
        return response


