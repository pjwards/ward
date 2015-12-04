__author__ = "Donghyun Seo"
__copyright__ = "Copyright ⓒ 2015, All rights reserved."
__email__ = "egaoneko@naver.com"


def application(env, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    return [b"Hello World"] # python3
