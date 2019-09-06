import os
import subprocess
from utils.cd import cd

def _run_cmd(path, cmd):
    with cd(path):
        res = subprocess.run(cmd, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, check=True, text=True)

        return res.stdout

class SingleParsedStatus(object):

    def __init__(self, raw : str):
        self.raw_status = raw[0:2]
        self.path = raw[3:]

    def is_conflict(self):
        xy = self.raw_status
        return 'U' in xy or xy in ['DD', 'AA']

    def __repr__(self):
        return self.raw_status + ' ' + self.path
    
    __str__ = __repr__

class Status(object):

    def __init__(self, raw : list):
        self.files = [SingleParsedStatus(line) for line in raw]

    def has_conflicts(self):
        return any(map(SingleParsedStatus.is_conflict, self.files))

    def is_clean(self):
        return len(self.files) == 0

    def __repr__(self):
        return str(self.files)
    
    __str__ = __repr__


class Git(object):

    def __init__(self, path, user=None, password=None):
        self.path = path
        self.user = user
        self.password = password

    def status(self):
        # Get porcelained status
        status = _run_cmd(self.path, 'git status --porcelain'.split(' ')).splitlines()
        # Parse status
        return Status(status)
