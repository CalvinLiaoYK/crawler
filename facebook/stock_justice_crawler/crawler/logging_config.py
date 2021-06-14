import sys
import logging
from pathlib import Path

formatter = logging.Formatter('[%(asctime)s][%(levelname)s] %(message)s')


def console_hdlr():
    _console_hdlr = logging.StreamHandler(sys.stdout)
    _console_hdlr.setFormatter(formatter)
    return _console_hdlr


def file_hdlr(log_path, logger_name):
    Path(log_path).mkdir(parents=True, exist_ok=True)
    _file_hdlr = logging.FileHandler((Path(log_path) / f'{logger_name}.log'), encoding='utf-8')
    _file_hdlr.setFormatter(formatter)
    return _file_hdlr
