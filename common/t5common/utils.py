import logging
import os
import sys

def parse_logger(string, stream=sys.stderr, level='info'):
    if not string:
        ret = logging.getLogger()
        hdlr = logging.StreamHandler(stream)
    else:
        ret = logging.getLogger(string)
        hdlr = logging.FileHandler(string)

    ret.setLevel(getattr(logging, level.upper()))
    ret.addHandler(hdlr)
    hdlr.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

    return ret


def get_logger(level='info'):
    return parse_logger('', level=level)


def read_token(path):
    """Helper for reading token or password files"""
    with open(os.path.expandvars(path), 'r') as f:
        return f.read().strip()
