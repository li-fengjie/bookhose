from django.http import JsonResponse


class HttpCode(object):
    ok = 200
    paramerror = 400
    unauth = 403
    mathoderror = 405
    severerror = 500


def result(code=HttpCode.ok, message="", data=None, kwargs=None):
    json_dict = {"code": code, "message": message, "data": data}
    if kwargs and isinstance(kwargs, dict) and kwargs.keys():
        json_dict.update(kwargs)
    return JsonResponse(json_dict)


def ok():
    return result()


def params_error(message="", data=None):
    return result(code=HttpCode.paramerror, message=message, data=data)


def unauth_error(message="", data=None):
    return result(code=HttpCode.paramerror, message=message, data=data)


def method_error(message="", data=None):
    return result(code=HttpCode.mathoderror, message=message, data=data)


def sever_error(message="", data=None):
    return result(code=HttpCode.severerror, message=message, data=data)
