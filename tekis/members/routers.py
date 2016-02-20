class MembersRouter(object):
    """
    A router to control all database operations on models in the
    members application.
    """
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'members':
            return 'members'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'members':
            return 'members'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if (obj1._meta.app_label == 'members' and
            obj2._meta.app_label == 'members'):
           return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'members':
            return db == 'members'
        return None
