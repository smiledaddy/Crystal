# -*- coding: utf-8 -*-
"""
    Multalisk Adapter module
    ~~~~~~~~~~~~~~~~~~~~~~~~

    used to transform database structure from origin data to multalisk data.
    This module provide a cron job interface to run transform scripts which
    was defined by business.

"""
from armory.ghost.timer import ArmoryCron


class Adapter(object):

    def __init__(self, target=None, broker='redis://localhost:6379/1'):
        self.cron_obj = ArmoryCron.getInstance(broker=broker)
        if target:
            self.register(target)

    def register(self, *args):
        '''register a func - schedule pair/tuple or func:schedule dict'''
        if len(args) > 1:
            self.cron_obj.timer(args[1])(args[0])
        elif isinstance(args[0], dict):
            for target_func, schedule in args[0].iteritems():
                self.cron_obj.timer(schedule)(target_func)
        elif isinstance(args[0], tuple) and len(args[0]) == 2:
            self.cron_obj.timer(args[0][1])(args[0][0])
        else:
            raise ValueError('args should be a func-schedule pair or dict')

    def run(self, worker_num=2):
        self.cron_obj.run(worker_num)


if __name__ == "__main__":
    def test_func():
        print 'do data transform...'

    k = Adapter({test_func: '33 2 * * *'})
    k.run()
