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

DEFAULT_NUMBER_OF_WORKERS = 2

def get_logging_level():
    # Default to error
    logging_level = logging.ERROR

    try:
        logging_level = os.environ['WORKER_LOGGING_LEVEL']
    except KeyError:
        pass

    return logging_level

logging.basicConfig(level=get_logging_level()) 

def get_number_of_workers():
    worker_count = DEFAULT_NUMBER_OF_WORKERS

    try:
        worker_count = int(os.environ['NUMBER_OF_WORKERS'])
    except KeyError:
        pass

    return worker_count

if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    number_of_workers = get_number_of_workers()

    logger.debug('Initialising workers...')
    logger.debug('  worker count = %s', number_of_workers)

    with Connection(connection):
        worker = Worker(list(map(Queue, listen)))

        workers = []

        for i in range(number_of_workers):
            processor = multiprocessing.Process(target=worker.work)

            workers.append(processor)
            processor.start()

    logger.debug('Workers initialised.')
