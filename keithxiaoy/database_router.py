import random


class ClientRouter:
    """
    A router to control all database operations on models in the
    client application.
    """

    def db_for_read(self, model, **hints):
        """
        Attempts to read client models go to client.
        """
        if model._meta.app_label == 'client':
            return 'client'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write client models go to client.
        """
        if model._meta.app_label == 'client':
            return 'client'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the client app is involved.
        """
        if obj1._meta.app_label == 'client' or \
                obj2._meta.app_label == 'client':
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the client app only appears in the 'client'
        database.
        """
        if app_label == 'client':
            return db == 'client'
        return None


class PrimaryReplicaRouter:
    def db_for_read(self, model, **hints):
        """
        Reads go to a randomly-chosen replica.
        """
        return random.choice(['primary'])

    def db_for_write(self, model, **hints):
        """
        Writes always go to primary.
        """
        return 'primary'

    def allow_relation(self, obj1, obj2, **hints):
        """
        Relations between objects are allowed if both objects are
        in the primary/replica pool.
        """
        db_list = ('primary',)
        if obj1._state.db in db_list and obj2._state.db in db_list:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        All non-auth models end up in this pool.
        """
        return True
