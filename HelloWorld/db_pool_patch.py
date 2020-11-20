# -*- coding: utf-8 -*-

from django.conf import settings
from sqlalchemy.pool import manage

POOL_PESSIMISTIC_MODE = getattr(settings, "DJ_ORM_POOL_PESSIMISTIC", False)
POOL_SETTINGS = getattr(settings, 'DJ_ORM_POOL_OPTIONS', {})
POOL_SETTINGS.setdefault("recycle", 3600)


def is_iterable(value):
    """Check if value is iterable."""
    try:
        _ = iter(value)
        return True
    except TypeError:
        return False


class HashableDict(dict):
    def __hash__(self):
        items = [(n, tuple(v)) for n, v in self.items() if is_iterable(v)]
        return hash(tuple(items))


class ManagerProxy(object):
    def __init__(self, manager):
        self.manager = manager

    def __getattr__(self, key):
        return getattr(self.manager, key)

    def connect(self, *args, **kwargs):
        if 'conv' in kwargs:
            kwargs['conv'] = HashableDict(kwargs['conv'])

        if 'ssl' in kwargs:
            kwargs['ssl'] = HashableDict(kwargs['ssl'])

        return self.manager.connect(*args, **kwargs)


def patch_mysql():
    from django.db.backends.mysql import base as mysql_base

    if not hasattr(mysql_base, "_Database"):
        mysql_base._Database = mysql_base.Database
        manager = manage(mysql_base._Database, **POOL_SETTINGS)
        mysql_base.Database = ManagerProxy(manager)


def patch_sqlite3():
    from django.db.backends.sqlite3 import base as sqlite3_base

    if not hasattr(sqlite3_base, "_Database"):
        sqlite3_base._Database = sqlite3_base.Database
        sqlite3_base.Database = manage(sqlite3_base._Database, **POOL_SETTINGS)


def install_patch():
    patch_mysql()
    patch_sqlite3()