import logging
from django.views import View


class MyView(View):
    """
    View with logger
    """
    def __init__(self, **kwargs):
        super(MyView, self).__init__(**kwargs)
        logger_name = f"django.{self.__class__.__module__}.{self.__class__.__name__}"
        self.logger = logging.getLogger(logger_name)
