import sys
import logging

__all__ = ['nolog', 'log', 'debug']

logger = logging.getLogger('aoc')


def log():
    logger.disabled = False
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)


def nolog():
    logger.disabled = True


def debug(*args):
    logger.info(*args)
