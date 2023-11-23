import logging


class CustomFilter(logging.Filter):
    def filter(self, record):
        return len(record.msg.split()) % 2


conf = {
    "version": 1,
    "formatters": {
        "file_formatter": {
            "format": "%(asctime)s : %(levelname)s : %(name)s : %(filename)s : %(message)s"
        },
        "stream_formatter": {
            "format": "%(asctime)s : %(levelname)s : %(name)s : %(message)s"
        },
    },
    "handlers": {
        "stream_handler": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "stream_formatter",
        },
        "file_handler": {
            "class": "logging.FileHandler",
            "level": "DEBUG",
            "formatter": "file_formatter",
            "filename": "09/cache.log",
            "mode": "w",
        },
    },
    "loggers": {
        "": {
            "level": "DEBUG",
            "handlers": ["file_handler"]
        },
    }
}
