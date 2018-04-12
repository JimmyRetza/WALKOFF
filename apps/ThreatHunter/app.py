from apps import App, action
from .db import ThreatHunterDb, Autorun, AutorunConfig


class ThreatHunter(App):
    def __init__(self, app_name='', device=''):
        super(App, self).__init__(app_name, device)
        self.db = ThreatHunterDb(self.device.fields['db_path'])

    @action
    def add_autoruns(self, autoruns, is_baseline=False):
        config = self.db.session.quuery(AutorunConfig).first()
        for autorun in autoruns:
            values = {k.lower(): v for k, v in autorun.items()}
            autorun = Autorun(**values)
            autorun.set_is_signature_unverified()
            autorun.set_is_suspicious_path(
                suspicious_path_elements=config.suspicious_paths,
                min_executable_length=config.min_executable_length)
            autorun.is_baseline = is_baseline
            self.db.session.add(autorun)
        self.db.session.commit()
        return 'Success'
