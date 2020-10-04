import logging
from logging import DEBUG, INFO

def get_logger(output_dir: str = None,
               level=DEBUG):
    logger = logging.getLogger(__name__)
    logger.setLevel(level)

    formatter = logging.Formatter('[%(asctime)s]%(levelname)s: line-no: %(lineno)d: %(message)s')
    s_handler = logging.StreamHandler()
    s_handler.setFormatter(formatter)
    logger.addHandler(s_handler)

    if output_dir is not None:
        f_handler = logging.FileHandler(f"{output_dir}/log.log")
        f_handler.setFormatter(formatter)
        logger.addHandler(f_handler)

    return logger


