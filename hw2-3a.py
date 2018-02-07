#!/usr/bin/env python

from collections import namedtuple

class Machine:
    def __init__(self, number):
        self.number = number
        self.jobs = []
        self.last_completion_time = 0

    def add(self, job):
        self.jobs.append(job)
        self.last_completion_time += job.processing_time

    def completion_times(self):
        cumulative_completion_time = 0
        completion_times = []
        for j in self.jobs:
            cumulative_completion_time += j.processing_time
            completion_times.append(cumulative_completion_time) 
        return completion_times

class Job(namedtuple('Job', ['number', 'processing_time'])):
    __slots__ = ()
    def __str__(self):
        return "(Job %d/duration %d)" % (self.number, self.processing_time)
    def __repr__(self):
        return self.__str__()


parameters = {}
execfile("./hw2-3.dzn", {}, parameters)

number_of_machines = parameters['number_of_machines']
number_of_jobs = parameters['number_of_jobs']
processing_time = parameters['processing_time']
assert number_of_jobs == len(processing_time)

machines = [Machine(i) for i in xrange(1, number_of_machines+1)]
jobs = [Job(number=i, processing_time=v)
    for i, v in enumerate(processing_time)
]
for j in sorted(jobs, key=lambda j: j.processing_time):
    min(machines, key=lambda v: v.last_completion_time).add(j)

for m in machines:
    print "\n\t".join([
        'Machine %d:',
        '%s',
        'completion times: %s',
        'last completion time: %d'
    ]) % (m.number, m.jobs, m.completion_times(), m.last_completion_time)
print "Sum of all completion times:", \
    sum([sum(m.completion_times()) for m in machines])
