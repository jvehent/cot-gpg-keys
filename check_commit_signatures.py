#!/usr/bin/env python
"""Check the signatures on git commits.

As currently written, the latest non-merge-commit must be signed.  If you sign
a commit, you're signing off on all changes since the last signed commit.
"""
import logging
import os
import re
import subprocess
import sys

# This dict will need to be updated to allow for more committers.
# If you update this dict, you also need to update the whitelist in puppet.
VALID_KEY_IDS = {
    "FC829B7FFAA9AC38": "asasaki@mozilla.com",
}
REGEX = re.compile(' using [A-Z]+ key( ID)? (0x)?(?P<keyid>[A-F0-9]*)$')
log = logging.getLogger(__name__)


def main(name=None):
    if name not in (None, "__main__"):
        return
    # logging
    if os.environ.get('VERBOSE'):
        log.setLevel(logging.DEBUG)
        log.addHandler(logging.StreamHandler())
    # get output from `git log`
    output = subprocess.check_output(
        ["git", "log", "--no-merges", "--format='%H:%GG'"]
    ).decode('utf-8')
    lines = output.splitlines()
    keyid = None
    line = lines[0]
    # the first line should look like SHA:gpg:...
    parts = line.replace("'", "").split(':')
    sha = parts[0]
    if parts[1] == 'gpg':
        for line in lines:
            line = line.replace("'", "")
            log.debug(line)
            if not line.startswith(sha) and not line.startswith("gpg:"):
                break
            m = REGEX.search(line)
            if m:
                keyid = m.groupdict()['keyid']
                if keyid not in VALID_KEY_IDS.keys():
                    message = "Latest commit {} is signed by an invalid key {}!".format(sha, keyid)
                    break
                else:
                    print("{} is signed by {} ({})".format(sha, keyid, VALID_KEY_IDS[keyid]))
                    sys.exit(0)
    if not keyid:
        message = "Latest commit {} is not signed!\nCommits must be gpg signed: `git commit -S[<keyid>]`".format(sha)
    raise Exception(message)


main(name=__name__)
