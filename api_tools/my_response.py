import json
from django.http import HttpResponse, StreamingHttpResponse


class MyJsonResponse(HttpResponse):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('content_type', 'application/json')
        super(MyJsonResponse, self).__init__(**kwargs)
        self._data = None
        self._error = None
        self.data = {}  # init empty content

    @property
    def data(self):
        return self._data

    @property
    def error(self):
        return self._error

    @data.setter
    def data(self, data):
        self._data = data
        result = {
            'success': True,
            'data': data
        }
        self.content = json.dumps(result)

    @error.setter
    def error(self, error):
        """
        generate error code and msg
        :param error: the param is a tuple that contain error code and message
        :return:
        """
        code, msg = error
        result = {
            'success': False,
            'data': {},
            'err_code': code,
            'msg': msg
        }
        self.content = json.dumps(result)
        self._error = error

    def set_data(self, data):
        result = {
            'success': True,
            'data': data
        }
        self.content = json.dumps(result)

    def set_error(self, code, msg):
        result = {
            'success': False,
            'data': {},
            'err_code': code,
            'msg': msg
        }
        self.content = json.dumps(result)


class PDFResponse(HttpResponse):
    def __init__(self, **kwargs):
        super(PDFResponse, self).__init__(**kwargs)
        self['Content-Type'] = 'application/pdf'
        self['Content-Disposition'] = 'inline; filename="download.pdf"'


class ExcelResponse(StreamingHttpResponse):
    def __init__(self, file_path, file_name, *args, **kwargs):
        super(ExcelResponse, self).__init__(self.file_iterator(file_path), *args, **kwargs)
        self['Content-Type'] = 'application/vnd.ms-excel'
        self['Content-Disposition'] = f'attachment;filename="{file_name}"'

    @staticmethod
    def file_iterator(file_name, chunk_size=512):
        """
        # 用于形成二进制数据
        :param file_name:
        :param chunk_size:
        :return:
        """
        with open(file_name, 'rb') as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break
