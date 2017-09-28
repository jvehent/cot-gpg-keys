#!/usr/bin/env python
""" Test for expiring GPG keys in puppet and cot-gpg-keys.

This script requires `arrow`, `requests` and gpg.

Attributes:
    WARNING_THRESHOLD (int): warn if any keys expire in less than this many days.
    ERROR_THRESHOLD (int): error if any keys expire in less than this many days.
    PUPPET_URL (str): the url to download the puppet pubkeys from.

"""
from __future__ import print_function

import arrow
import fnmatch
import os
import requests
import re
import subprocess
import sys
import zipfile

WARNING_THRESHOLD = 60
ERROR_THRESHOLD = 30
PUPPET_URL = "https://hg.mozilla.org/build/puppet/archive/production.zip/modules/scriptworker/files/git_pubkeys/"
EXPIRE_REGEX = re.compile('expires: (\d{4}-\d{2}-\d{2})')


def find_pubkeys(path):
    """ Recursively find files ending with `.pub` in `path`.

    Arguments:
        path (str): the directory to search

    Returns:
        list: the list of pubkey paths

    """
    matches = []
    for root, dirnames, filenames in os.walk(path):
        for filename in fnmatch.filter(filenames, '*.pub') + fnmatch.filter(filenames, '*.asc'):
            matches.append(os.path.join(root, filename))
    return matches


def download_extract_puppet_pubkeys():
    r = requests.get(PUPPET_URL, stream=True)
    r.raise_for_status()
    with open('puppet.zip', 'wb') as fh:
        for chunk in r.iter_content(chunk_size=128):
            fh.write(chunk)
    r.close()
    z = zipfile.ZipFile('puppet.zip')
    z.extractall()


def check_expiration(path):
    # run `gpg KEY.pub`, find expiration markers, check against arrow and
    # thresholds
    print(path)
    output = subprocess.check_output(['gpg', path]).decode('utf-8')
    level_config = [
        {'msg': 'Good.'},
        {'msg': 'WARNING: %(path)s expires within %(warning_threshold)d days: %(expiry)s!'},
        {'msg': 'ERROR: %(path)s expires within %(error_threshold)d days: %(expiry)s!'},
    ]
    level_int = 0
    earliest_expiry = None
    for line in output.splitlines():
        m = EXPIRE_REGEX.search(line)
        if m:
            a = arrow.get(m.group(1))
            if not earliest_expiry:
                earliest_expiry = a
            elif earliest_expiry > a:
                earliest_expiry = a
    now = arrow.utcnow()
    if earliest_expiry:
        print("Earliest expiry is {} .".format(earliest_expiry))
        if now.replace(days=ERROR_THRESHOLD) > earliest_expiry:
            level_int = 2
        elif now.replace(days=WARNING_THRESHOLD) > earliest_expiry:
            level_int = 1
    else:
        print("No expiration_markers.")
    repl_dict = {
        'path': path,
        'warning_threshold': WARNING_THRESHOLD,
        'error_threshold': ERROR_THRESHOLD,
        'expiry': earliest_expiry,
    }
    if level_config[level_int].get('msg'):
        msg = level_config[level_int]['msg'] % repl_dict
        print(msg)
    print()

    return level_int


def main():
    TOPDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    download_extract_puppet_pubkeys()
    pubkeys = find_pubkeys(TOPDIR)
    status = 0
    for pubkey in sorted(pubkeys):
        local_status = check_expiration(pubkey)
        if local_status > status:
            status = local_status
    sys.exit(status)

__name__ == '__main__' and main()
