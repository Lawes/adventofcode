import sys
import logging

__all__ = ['nolog', 'log', 'debug', 'is_log_enable']

logger = logging.getLogger('aoc')


def log():
    logger.disabled = False
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)


def nolog():
    logger.disabled = True


def is_log_enable():
    return not logger.disabled


def debug(*args):
    logger.info(*args)
