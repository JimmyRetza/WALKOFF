import ntpath
from uuid import UUID

from sqlalchemy import Column, Boolean, DateTime, String, Integer
from sqlalchemy_utils import ScalarListType

from .base import ThreatHunterBase, BaselineMixin, WhitelistMixin

suspicious_paths_default = ('programdata', 'appdata', 'recycle.bin')


class AutorunConfig(ThreatHunterBase):
    id = Column(Integer, primary_key=True, autoincrement=True)
    suspicious_paths = Column(ScalarListType(), default=suspicious_paths_default)
    min_executable_length = Column(Integer, default=5)


class Autorun(ThreatHunterBase, BaselineMixin, WhitelistMixin):
    __tablename__ = 'autorun'
    id = Column(Integer, primary_key=True, autoincrement=True)
    time = Column(DateTime)
    entry_location = Column(String)
    entry = Column(String)
    is_enabled = Column(Boolean)
    category = Column(String)
    profile = Column(String)
    description = Column(String)
    signer = Column(String)
    company = Column(String)
    image_path = Column(String)
    version = Column(String)
    launch_string = Column(String)
    is_signer_verified = Column(Boolean)
    is_image_path_suspicious = Column(Boolean)

    def set_is_suspicious_path(self, suspicious_path_elements=suspicious_paths, min_executable_length=5):
        image_path = self.image_path.lower()
        self.is_image_path_suspicious = (
            any(suspicious_path in image_path for suspicious_path in suspicious_path_elements)
            or self.is_executable_suspicious_executable(image_path, min_executable_length=min_executable_length))

    def set_is_signature_unverified(self):
        self.is_signer_verified = 'Verified' in self.signer

    @staticmethod
    def is_executable_suspicious_executable(path, min_executable_length=5):
        head, tail = ntpath.split(path)
        executable = tail or ntpath.basename(head)
        executable_path = executable.split('.')[0]
        if executable_path < min_executable_length:
            return True
        try:
            UUID(executable_path)
            return True
        except ValueError:
            pass
        return False
