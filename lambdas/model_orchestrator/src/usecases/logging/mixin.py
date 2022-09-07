from . import JsonLogger


class LoggableMixin:
    @classmethod
    def get_logger(cls):
        return JsonLogger(cls)

    @classmethod
    def info(cls, *args, **kwargs):
        cls.get_logger().info(*args, **kwargs)

    @classmethod
    def exception(cls, *args, **kwargs):
        cls.get_logger().exception(*args, **kwargs)
