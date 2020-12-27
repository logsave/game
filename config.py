import logging


# Log Config
LogLevel=logging.ERROR
LogFile=""
LogFormat="[%(levelname)s] %(asctime)-15s  %(message)s"

config = {
    'mysql': {
        'host': 'localhost',
        'port': 3306
    }
    'mongo': {
        'uri': 'localhost',
        'user': 'logsave'
    }
}