from pythonjsonlogger.jsonlogger import JsonFormatter


class HJsonLogFormat(JsonFormatter):
    def __init__(self, *args, **kwargs):
        # 继承JsonFormatter， 传入json_ensure_ascii， 解决中文日志乱码问题
        super(HJsonLogFormat, self).__init__(json_ensure_ascii=False, *args, **kwargs)