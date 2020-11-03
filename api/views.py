from api_tools.my_view import MyView
from api_tools.my_response import MyJsonResponse, PDFViewResponse, TestDownload

# Create your views here.


class TestJson(MyView):
    def post(self, request):
        resp = MyJsonResponse()
        print("POST", request.POST)
        print("Data", request.data)
        return resp


class TestPDF(MyView):
    def get(self, request):
        self.logger.info("view pdf")
        return PDFViewResponse("/Users/yaoshao/Desktop/app_source_addr.pdf", "app_source_addr.pdf")


class TestDownloadExcel(MyView):
    def get(self, request):
        return TestDownload("/Users/yaoshao/Desktop/1.xlsx", "1.xlsx")


class TestDownloadPDF(MyView):
    def get(self, request):
        return TestDownload("/Users/yaoshao/Desktop/app_source_addr.pdf", "app_source_addr.pdf")
