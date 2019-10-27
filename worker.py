from redis import Redis
from rq import Worker, Queue, Connection
import multiprocessing

listen = ['service']
connection = Redis()

MAX_WORKERS = 2

if __name__ == '__main__':
    with Connection(connection):
        worker = Worker(list(map(Queue, listen)))

        workers = []

        for i in range(MAX_WORKERS):
            processor = multiprocessing.Process(target=worker.work)

            workers.append(processor)
            processor.start()
