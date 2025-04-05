import logging
class MyLogging:
    _instance=None

    """Safely log exceptions without interfering with PyQt internals."""


    def __init__(self):

        logging.basicConfig(filename='app_log.txt',level=logging.INFO,format='%(asctime)s - %(levelname)s - %(message)s')


    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(MyLogging, cls).__new__(cls)
        return cls._instance

    def log_error(msg):
        logging.error(msg=msg)
    def log_info(msg):
        logging.info(msg=msg)
    def log_warning(msg):
        logging.warning(msg=msg)


