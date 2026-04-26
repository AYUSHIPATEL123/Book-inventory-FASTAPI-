import logging
import logging.config


LOGGING_CONFIG = {
    "version":1,

    # "disable_existing_loggers": False,

    "formatters":{
        "default":{
            "format":"%(asctime)s - %(filename)s - %(levelname)s - %(name)s - %(message)s"
        },
    },

    "handlers":{
        "file":{
            # "class":"logging.FileHandler",
            "class":"logging.handlers.RotatingFileHandler",
            "filename":"./app.log",
            "maxBytes":1048576,  # 1 mb storage
            "backupCount": 3,
            "formatter":"default",
        },
    },

    "root":{
        "level":"INFO",
        "handlers":['file',],
    },

    "loggers":{
        "uvicorn.error":{
            "level":"WARNING",
            "propagate": True,
        },
        "sqlalchemy.engine":{
            "level":"WARNING",
            "propagate":False,
        },
        "uvicorn.access":{
            "level":"WARNING",
            "propagate": False,
        },
    },
    
}


logging.config.dictConfig(LOGGING_CONFIG)


def make_logger(name):
    logger = logging.getLogger(name)
    return logger
