from django.http import JsonResponse

def error_response(error_code,error_msg):
    """
    process_error_msg
    """
    data = {
        'error_msg':error_msg,
    }
    response = JsonResponse(data=data)
    response.status_code = error_code
    return response

def login_req(view_func):
    def _wrapper(request,*args, **kwargs):
        if request.user.is_authenticated :
            return view_func(request,*args, **kwargs)
        return error_response(401,"not authenticated")
    return _wrapper
