# -*- coding: utf-8 -*-
"""
    worker
    ~~~~~~~~~
    Kicks off workers for the processing queues.
"""

import os
import logging
import multiprocessing

from redis import Redis
from rq import Worker, Queue, Connection

listen = ['service']
connection = Redis()

MAX_WORKERS = 2

def get_logging_level():
    # Default to error
    logging_level = logging.ERROR

    try:
        logging_level = os.environ['WORKER_LOGGING_LEVEL']
    except KeyError:
        pass

    return logging_level

logging.basicConfig(level=get_logging_level()) 

if __name__ == '__main__':
    logger = logging.getLogger(__name__)

    logger.debug('Initialising workers...')
    logger.debug('  worker count = %s', MAX_WORKERS)

    with Connection(connection):
        worker = Worker(list(map(Queue, listen)))

        workers = []

        for i in range(MAX_WORKERS):
            processor = multiprocessing.Process(target=worker.work)

            workers.append(processor)
            processor.start()

    logger.debug('Workers initialised.')
