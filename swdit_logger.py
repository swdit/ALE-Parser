#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
based on 'logging' module
this file contains a function that returns a logger with a customized formatter.
It is also more robust against multiple calls of the function.
"""

import logging


# customized logger for colored output
class CustomFormatter(logging.Formatter):
    grey = "\x1b[0;37m"
    yellow = "\x1b[33m"
    red = "\x1b[31;1m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "%(asctime)s - %(levelname)s - %(message)s"

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: grey + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, "%Y-%m-%d %H:%M:%S")
        return formatter.format(record)


def get_logger(name, level="INFO"):
    # convert log-level string into log-level value
    numeric_level = getattr(logging, level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f"Ungültiges Log Level: {level}")

    # check logger configuration
    logger = logging.getLogger(name)
    logger.setLevel(numeric_level)

    # check for already existing handlers
    if not logger.handlers:
        # create and add handler
        ch = logging.StreamHandler()
        ch.setFormatter(CustomFormatter())
        logger.addHandler(ch)

    return logger
