import random


class MasterSlaveRouter(object):

    def db_for_read(self, model, **hints):
        return random.choice(['default'])

    def db_for_write(self, model, **hints):
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        return True

    def allow_syncdb(self, db, model):
        return True