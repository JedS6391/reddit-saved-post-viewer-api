# -*- coding: utf-8 -*-
"""
    service
    ~~~~~~~~~
    This module contains the logic for interacting with the worker queue.
"""

from rq import Queue
from redis import Redis

from api.queue.workers import Worker

class QueueService:
    """ Enscapsulates the interaction with a worker queue. """

    def __init__(self, timeout=500):
        self.connection = Redis()
        self.queue = Queue('service', connection=self.connection)
        self.timeout = timeout

    def enqueue(self, worker, meta=None):
        """ Adds the given worker to the job queue and returns the associated job. """

        if not isinstance(worker, Worker):
            raise ValueError('Cannot enqueue instances that are not subclasses of Worker.')

        job = self.queue.enqueue(worker.process, ttl=self.timeout)

        # Create an association between the job and the worker token
        job.meta['token'] = worker.token
        job.save_meta()

        return job

    def status(self, job_id):
        """ Provides status information for the job with the given ID. """

        job = self.queue.fetch_job(job_id)

        if not job:
            return None

        return dict(state=job.get_status(), result=job.result, meta=job.meta)
