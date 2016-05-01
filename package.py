#!/usr/bin/python

import argparse
import os
import tempfile
import requests
import subprocess
import logging
import json
import sys

URL = 'https://api.github.com/repos/rqlite/rqlite/releases'

def run(command, allow_failure=False, shell=False):
    out = None
    logging.debug("{}".format(command))
    try:
        if shell:
            out = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=shell)
        else:
            out = subprocess.check_output(command.split(), stderr=subprocess.STDOUT)
        out = out.decode('utf-8').strip()
    except subprocess.CalledProcessError as e:
        if allow_failure:
            logging.warn("Command '{}' failed with error: {}".format(command, e.output))
            return None
        else:
            logging.error("Command '{}' failed with error: {}".format(command, e.output))
            sys.exit(1)
    except OSError as e:
        if allow_failure:
            logging.warn("Command '{}' failed with error: {}".format(command, e))
            return out
        else:
            logging.error("Command '{}' failed with error: {}".format(command, e))
            sys.exit(1)
    else:
        return out

def get_current_commit(short=False):
    command = None
    if short:
        command = "git log --pretty=format:'%h' -n 1"
    else:
        command = "git rev-parse HEAD"
    out = run(command)
    return out.strip('\'\n\r ')

def get_current_branch():
    command = "git rev-parse --abbrev-ref HEAD"
    out = run(command)
    return out.strip()

def get_system_arch():
    arch = os.uname()[4]
    if arch == "x86_64":
        arch = "amd64"
    return arch

class Parser(object):
    def __init__(self, text):
        self.text = text

    def parse(self):
        self.json = json.loads(self.text)

    def release_id(self, tag):
        for release in self.json:
            if release['tag_name'] == tag:
                return release['id']
        return None

    def upload_url(self, tag):
        for release in self.json:
            if release['tag_name'] == tag:
                return release['upload_url']
        return None

def parse_args():
    parser = argparse.ArgumentParser(description='Publish a rqlite release to GitHub.')
    parser.add_argument('tag', metavar='TAG', type=str,
                       help='tag in the form "vX.Y.Z"')
    parser.add_argument('token', metavar='TOKEN', type=str,
                       help='GitHub API token')

    return parser.parse_args()

def main():
    args = parse_args()

    r = requests.get(URL)
    if r.status_code != 200:
        print 'failed to download release information'
        sys.exit(1)

    p = Parser(r.text)
    p.parse()
    release_id = p.release_id(args.tag)
    if release_id == None:
        print 'unable to determine release ID for tag %s' % args.tag
        sys.exit(1)

    print get_current_commit()
    print get_current_branch()
    print get_system_arch()

if __name__ == '__main__':
    main()
