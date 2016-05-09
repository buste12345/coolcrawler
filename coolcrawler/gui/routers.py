class guiDBRouter(object):
    """
    A router to control gui db operations
    """
    def db_for_read(self, model, **hints):
        "Point all operations on gui models to 'monguito'"
        from django.conf import settings
        if not settings.DATABASES.has_key('gui'):
            return None
        if model._meta.app_label == 'gui':
            return 'monguito'
        return None

    def db_for_write(self, model, **hints):
        "Point all operations on gui models to 'monguito'"
        from django.conf import settings
        if not settings.DATABASES.has_key('gui'):
            return None
        if model._meta.app_label == 'gui':
            return 'monguito'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        "Allow any relation if a model in gui is involved"
        from django.conf import settings
        if not settings.DATABASES.has_key('gui'):
            return None
        if obj1._meta.app_label == 'gui' or obj2._meta.app_label == 'gui':
            return True
        return None

    def allow_syncdb(self, db, model):
        "Make sure the gui app only appears on the 'gui' db"
        from django.conf import settings
        if not settings.DATABASES.has_key('gui'):
            return None
        if db == 'monguito':
            return model._meta.app_label == 'gui'
        elif model._meta.app_label == 'gui':
            return False
        return None