# -*- coding: utf-8 -*-

from django.conf import settings
from sqlalchemy import event, exc
from sqlalchemy.pool import Pool

from log import logger


@event.listens_for(Pool, "checkout")
def _on_checkout(dbapi_connection, connection_record, connection_proxy):
    logger.debug("connection retrieved from pool")

    if settings.POOL_PESSIMISTIC_MODE:
        cursor = dbapi_connection.cursor()
        try:
            cursor.execute("SELECT 1")
        except:
            # raise DisconnectionError - pool will try
            # connecting again up to three times before raising.
            raise exc.DisconnectionError()
        finally:
            cursor.close()


@event.listens_for(Pool, "checkin")
def _on_checkin(*args, **kwargs):
    logger.debug("connection returned to pool")


@event.listens_for(Pool, "connect")
def _on_connect(*args, **kwargs):
    logger.debug("connection created")