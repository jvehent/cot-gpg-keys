# TaskCluster worker GPG key repo

This repo contains GPG pubkeys, used to validate the signature in the Taskcluster worker Chain of Trust artifact.

Commits to this repo must be signed by trusted keys.  The whitelist of valid gpg fingerprints for git commit signing is in puppet.

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

## Signing git commits

In your `~/.gitconfig`:
 - set your `user.signingkey` to your long keyid or fingerprint
 - set your `gpg.program` to the path to gpg.  I recommend the latest gpg 2.0.x.

In `./.git/config`:
 - set `commit.gpgSign = true` to sign commits to this repo by default.

You can also specify `git commit -S[<keyid>]` on the commandline, but the config pref means you don't have to remember.
