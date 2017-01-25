class Router(object):
    def db_for_read(self, model, **hints):
        if model._meta.model_name == 'articleotherdb':
            return 'other'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.model_name == 'articleotherdb':
            return 'other'
        return None

    def allow_migrate(self, db, app_label, model=None, **hints):
        if model:
            if model._meta.model_name == 'articleotherdb':
                return db == 'other'
            else:
                return db == 'default'
        return None
