[![Task Status](https://github.taskcluster.net/v1/repository/mozilla-releng/cot-gpg-keys/master/badge.svg)](https://github.taskcluster.net/v1/repository/mozilla-releng/cot-gpg-keys/master/latest)

# TaskCluster worker GPG key repo

This repo contains GPG pubkeys, used to validate the signature in the Taskcluster worker Chain of Trust artifact.

We use the latest revision that is tagged (a la `git describe`); that tag must be signed by a valid key.  The whitelist of valid gpg fingerprints for git commit signing is in [puppet](https://hg.mozilla.org/build/puppet/file/tip/modules/scriptworker/files/git_pubkeys).

## Directory structure

At the top level, we have

```
  docker-worker/
    subdir/  # datestring, timestamp, or ami-group ids, for cleanup purposes
      pubkey1
      pubkey2
      ...
    ...
  generic-worker/
    subdir/  # datestring, timestamp, or ami-group ids, for cleanup purposes
      pubkey1
      pubkey2
      ...
    ...
  scriptworker/
    trusted/
    valid/
```

## Tagging git commits

You need to have a [trusted gpg key](https://hg.mozilla.org/build/puppet/file/tip/modules/scriptworker/files/git_pubkeys) to perform this step!

In your `~/.gitconfig`:
 - set your `user.signingkey` to your long keyid or fingerprint
 - set your `gpg.program` to the path to gpg.  I recommend the latest gpg 2.0.x.

To tag,

```bash
# First make sure all changes since the last tag are legit!
git pull --ff-only --tags
PREVIOUS_TAG=`git describe --abbrev=0`
# check the signature of the previous tag
git tag -v "$PREVIOUS_TAG"
# check the commit logs between the previous tag and HEAD
git log "$PREVIOUS_TAG"..HEAD
# check the diff between the previous tag and HEAD
git diff "$PREVIOUS_TAG"
# if that all looks good, tag
DATE=`python -c "from __future__ import print_function; import datetime; d=datetime.datetime.utcnow(); print('%04d%02d%02d%02d%02d%02d'%(d.year,d.month,d.day,d.hour,d.minute,d.second))"`
git tag -s -m "production-$DATE" production-$DATE
git push --tags
# you also need to `git push --tags` to the upstream repo
git push git@github.com:mozilla-releng/cot-gpg-keys.git --tags
```

I added a `tag.sh` to do the above, minus the extra `git push`.

We no longer need to sign commits.

### Backing out changes

We pull with `--ff-only`, so non-fast-forward changes are not allowed.  Also, `git describe` shows the latest reachable revision that's tagged.  Therefore, if you need to back out changes,

- land the backout as a new commit
- tag the new commit

### Note: gpg keys with revoked subkeys will break

if `gpg --with-colons --list-sigs --with-fingerprint --with-fingerprint` contains any `rev` or `rvk` lines, that key will no longer be trusted to sign tags or other gpg keys in scriptworker.  Please generate a new key.
