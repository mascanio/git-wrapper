import os
import sys
import subprocess

from utils.cd import cd
from utils.shell_split import shell_split

class Error(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)

class GitError(Error):

    def __init__(self, stdout, stderr):
        self.stdout = stdout
        self.stderr = stderr
        self.message = f"""Git exception
STDOUT:
{stdout}
-------------------------------------------------------------------------------
STDERR:
{stderr}
"""
        Error.__init__(self, self.message)

class AuthenticationError(Error):
    def __init__(self):
        self.message = 'Git: invalid username or password.'
        Exception.__init__(self, self.message)


def _build_error(stdout, stderr):
    if 'remote: Invalid username or password.' in stderr.splitlines()[0]:
        return AuthenticationError()
    else:
        return GitError(stdout, stderr)

def _run_cmd(path, cmd, stdin=subprocess.DEVNULL, env=None):

    if type(cmd) == str:
        cmd = shell_split(cmd)

    with cd(path):
        res = subprocess.run(cmd, env=env, stdin=stdin, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if res.returncode != 0:
            raise _build_error(res.stdout, res.stderr)

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

    def __init__(self, path, remote, user=None, password=None):
        self.path = path
        self.user = user
        self.password = password
        self.remote = remote
        self.auth_remote = self._auth_remote()

    def _auth_remote(self):
        return f'https://{self.user}:{self.password}@{self.remote.split("https://")[1]}'

    def status(self):
        # Get porcelained status
        status = _run_cmd(self.path, 'git status --porcelain').splitlines()
        # Parse status
        return Status(status)

    def commit(self, commit_message):
        if self.status().is_clean():
            return
        res = _run_cmd(self.path, 'git commit -m "{}"'.format(commit_message.replace('"', '\\"')))

    def add_all(self):
        res = _run_cmd(self.path, 'git add -A')

    def get_current_branch(self):
        return _run_cmd(self.path, 'git symbolic-ref --short HEAD').strip()

    def push(self, branch):
        return _run_cmd(self.path, f'git push {self.auth_remote} {branch}')

    def pull(self, branch, rebase=False):
        return _run_cmd(self.path, f'git pull{" --rebase" if rebase else ""} {self.auth_remote} {branch}')

    def rebase_stash(self, branch):
        return _run_cmd(self.path, f'git pull --rebase --autostash {self.auth_remote} {branch}')

