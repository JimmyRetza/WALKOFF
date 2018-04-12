from sqlalchemy import Column, Boolean
from sqlalchemy.ext.declarative import declarative_base

ThreatHunterBase = declarative_base()


class BaselineMixin(object):
    is_baseline = Column(Boolean, default=False, nullable=False)


class WhitelistMixin(object):
    is_whitelist = Column(Boolean, default=False)