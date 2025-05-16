import logging

logging.basicConfig(filename="errors.log",
                    format='%(asctime)s-%(message)s',
                    filemode='w', encoding='utf-8')

logger = logging.getLogger()

logger.setLevel(logging.DEBUG)
