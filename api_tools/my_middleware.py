import logging
import json
import re
import time
from api_tools.my_response import MyJsonResponse


class MyMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response
        self.logger = logging.getLogger('django')
        self.logger_access = logging.getLogger('access')

    def process_exception(self, request, exception):
        path = request.path

        # api报错处理
        if re.search('^/api', path):
            self.logger.exception("View process failed for request: {} e: {}, body: {}".format(
                request.full_path,
                exception,
                self._format_body(request.body)
            ))

            resp = MyJsonResponse()
            resp.error = (-1, "Server error")
            return resp
        return None

    def process_view(self, request, view_func, view_args, view_kwargs):
        body = request.body
        format_body = self._format_body(body)
        path = request.path

        if request.method == 'POST':
            # 处理post请求，ajax和form data数据都储存到request.data
            try:
                if not request.POST:
                    data = json.loads(format_body)
                    setattr(request, "data", data)
                else:
                    setattr(request, "data", request.POST)
            except Exception as e:
                self.logger.warning(
                    f"Process view middleware, process json error, view: {view_func.__name__}, request body:{format_body} path: {path} e: {e}")
                resp = MyJsonResponse()
                resp.error = (-3, 'Json format error')
                return resp
        return None

    def process_response(self, request, response):
        """
        增加日志记录可以使用的字段
        :param request:
        :param response:
        :return:
        """
        logging_dict = {
            'duration': time.time() - request.timer,
            'client_ip': request.META.get('REMOTE_ADDR'),
            'x_forwarded_ip': request.META.get('HTTP_X_FORWARDED_FOR'),
            'path': request.full_path,
            'status': response.status_code,
            'http_user_agent': request.META.get('HTTP_USER_AGENT'),
            'server_name': request.META.get('SERVER_NAME'),
            'content_length': request.META.get('CONTENT_LENGTH'),
            'protocol': request.META.get('SERVER_PROTOCOL'),
        }
        self.logger_access.info("", extra=logging_dict)

    @staticmethod
    def _format_body(body):
        return body.decode('utf-8')

    def __call__(self, request):
        request.timer = time.time()
        request.full_path = request.path + request.META.get('QUERY_STRING')
        response = self.get_response(request)
        self.process_response(request, response)
        return response
