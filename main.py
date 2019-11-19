from __future__ import (absolute_import, division, print_function)

import os

import errno
import pty
import sys
from select import select


from os import devnull
from subprocess import Popen, PIPE, CalledProcessError
import subprocess
import click

# os.execvp('ssh', ['assh', '-i', '~/.ssh/flashtalking-aws-devops', 'ec2-user@34.244.200.168'])


def passthrough(cmd=None, interactive=False):
    masters, slaves = zip(pty.openpty(), pty.openpty())
    cmd = cmd.split()

    with Popen(cmd, stdin=slaves[0], stdout=slaves[0], stderr=slaves[1]) as p:
        for fd in slaves:
            os.close(fd) # no input
            readable = {
                masters[0]: sys.stdout.buffer, # store buffers seperately
                masters[1]: sys.stderr.buffer,
            }
        while readable:
            for fd in select(readable, [], [])[0]:
                try:
                    data = os.read(fd, 1024) # read available
                except OSError as e:
                    if e.errno != errno.EIO:
                        raise #XXX cleanup
                    del readable[fd] # EIO means EOF on some systems
                else:
                    if not data: # EOF
                        del readable[fd]
                    else:
                        if fd == masters[0]: # We caught stdout
                            click.echo(data.rstrip())
                        else: # We caught stderr
                            click.echo(data.rstrip(), err=True)
                        readable[fd].flush()
    for fd in masters:
        os.close(fd)
    return p.returncode

ENCODING = 'utf-8'


def check_output(popenargs, **kwargs):
    """Runs a program, waits for its termination and returns its output
    This function is functionally identical to python 2.7's subprocess.check_output,
    but is favored due to python 2.6 compatibility.
    Will be run through a shell if `popenargs` is a string, otherwise the command
    is executed directly.
    The keyword argument `decode` determines if the output shall be decoded
    with the encoding UTF-8.
    Further keyword arguments are passed to Popen.
    """

    do_decode = kwargs.pop('decode', True)
    kwargs.setdefault('stdout', PIPE)
    kwargs.setdefault('shell', isinstance(popenargs, str))

    if 'stderr' in kwargs:
        process = Popen(popenargs, **kwargs)
        stdout, _ = process.communicate()
    else:
        with open(devnull, mode='w') as fd_devnull:
            process = Popen(popenargs, stderr=fd_devnull, **kwargs)
            stdout, _ = process.communicate()

    if process.returncode != 0:
        error = CalledProcessError(process.returncode, popenargs)
        error.output = stdout
        raise error

    if do_decode and stdout is not None:
        stdout = stdout.decode(ENCODING)

    return stdout

#passthrough("fzf", True)
#    cmd = [
#        fzf, '-m',
#        '--query=a'
#    ]
#    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
#    out = proc.communicate('\n'.join(all_tasks))[0].splitlines()

#p1 = subprocess.Popen(['ls', '-ltr'], stdout=subprocess.PIPE,
                                        #      stderr=subprocess.PIPE)
#p2 = subprocess.Popen(['less'], stdin=p1.stdout)

def execute(program, args, **kwargs):
    """Executes a command in a subprocess and returns its standard output."""
    return (
            subprocess.run([program, *args], stdout=subprocess.PIPE, **kwargs)
            .stdout.decode()
            .strip()
    )

fzf_input = "\n".join(["a","b"]).encode()
aaa = execute("fzf", [], input=fzf_input)
import ptpdb
ptpdb.set_trace()
