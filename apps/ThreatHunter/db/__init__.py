from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.pool import NullPool

from walkoff.helpers import format_db_path

from .base import ThreatHunterBase

from .autorun import Autorun, AutorunConfig

__all__ = ['ThreatHunterBase', 'Autorun', 'AutorunConfig']


class ThreatHunterDb(object):
    instance = None

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super(ThreatHunterDb, cls).__new__(cls)
        return cls.instance

    def __init__(self, db_path):
        self.engine = create_engine(format_db_path('sqlite', db_path),
                                    connect_args={'check_same_thread': False}, poolclass=NullPool)
        self.connection = self.engine.connect()
        self.transaction = self.connection.begin()

        Session = sessionmaker()
        Session.configure(bind=self.engine)
        self.session = scoped_session(Session)

        Execution_Base.metadata.bind = self.engine
        Execution_Base.metadata.create_all(self.engine)

    def tear_down(self):
        self.session.rollback()
        self.connection.close()
        self.engine.dispose()



