from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.pool import NullPool
from sqlalchemy import Column, Boolean

from walkoff.helpers import format_db_path

ThreatHunterBase = declarative_base()


class ThreathunterDb(object):
    instance = None

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super(ThreathunterDb, cls).__new__(cls)
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


class BaselineMixin(object):
    is_baseline = Column(Boolean, default=False, nullable=False)


class WhitelistMixin(object):
    is_whitelist = Column(Boolean, default=False)



