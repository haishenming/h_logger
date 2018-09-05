import logging.config
import structlog
from structlog import configure, processors, stdlib, threadlocal
#
log_level_map = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warn': logging.WARN,
    'error': logging.ERROR,
    'critical': logging.CRITICAL
}

base_set = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'json': {
            'format': '%(asctime)s %(levelname)s %(pathname)s %(lineno)d %(message)s %(lineno)d',
            'datefmt': "%Y-%m-%d %H:%M:%S %Z",
            'class': 'pythonjsonlogger.jsonlogger.JsonFormatter'
        }
    },
    'handlers': {
        'stream': {
            'class': 'logging.StreamHandler',
            'formatter': 'json',
        }
    },
    'loggers': {
        'default': {
            'handlers': ['stream'],
        }
    }
}


class Logger:

    def __init__(self, logger_name='default', level='debug', filename=''):
        self.logger = logging.getLogger(logger_name)
        self.level = log_level_map.get(level)
        self.filename = filename
        self.log_set = self.__format_logger_set()
        logging.config.dictConfig(self.log_set)
        configure(
            # context_class=threadlocal.wrap_dict(dict),
            logger_factory=stdlib.LoggerFactory(),
            # wrapper_class=stdlib.BoundLogger,
            processors=[
                # stdlib.filter_by_level,
                # stdlib.add_logger_name,
                # stdlib.add_log_level,
                # stdlib.PositionalArgumentsFormatter(),
                # processors.TimeStamper(fmt="iso"),
                # processors.StackInfoRenderer(),
                # processors.format_exc_info,
                # processors.UnicodeDecoder(),
                stdlib.render_to_log_kwargs]
        )

    def __format_logger_set(self):
        logger_set = base_set
        level_set = {'level': self.level}
        logger_set['loggers']['default'].update(level_set)
        if self.filename:
            file_handler = {
                'file': {
                    'class': 'logging.FileHandler',
                    'formatter': 'json',
                    'filename': self.filename,
                    'mode': 'a'
                }
            }
            logger_set['handlers'].update(file_handler)
            logger_set['loggers']['default']['handlers'].append('file')
        return logger_set

    def __format_log_str(self):
        """
        :param 格式化输出对象
        """
        pass

    def __output_log(self, level, msg):
        getattr(self.logger, level)(msg)

    def debug(self, msg=''):
        self.__output_log('debug', msg)

    def info(self, msg=''):
        self.__output_log('info', msg)

    def warn(self, msg=''):
        self.__output_log('warn', msg)

    def error(self, msg=''):
        self.__output_log('error', msg)

    def critical(self, msg=''):
        self.__output_log('critical', msg)


if __name__ == '__main__':
    # log = Logger(filename='./log.log')
    log = Logger(filename='./log.log')

    log.info("debug")
