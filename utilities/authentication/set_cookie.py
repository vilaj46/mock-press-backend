from flask import make_response


def set_cookie():
    response = make_response('Setting a cookie')
    response.set_cookie('foo', 'bar', max_age=1)
    return response
