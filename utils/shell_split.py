import os
import sys
import subprocess
import shlex
import json  # json is an easy way to send arbitrary ascii-safe lists of strings out of python

def shell_split(cmd):
    """
    Like `shlex.split`, but uses the Windows splitting syntax when run on Windows.

    On windows, this is the inverse of subprocess.list2cmdline
    """
    if os.name == 'posix':
        return shlex.split(cmd)
    else:
        # TODO: write a version of this that doesn't invoke a subprocess
        if not cmd:
            return []
        full_cmd = '{} {}'.format(
            subprocess.list2cmdline([
                sys.executable, '-c',
                'import sys, json; print(json.dumps(sys.argv[1:]))'
            ]), cmd
        )
        ret = subprocess.check_output(full_cmd).decode()
        return json.loads(ret)
