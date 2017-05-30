#!/bin/bash

# add or remove worker types here
workertypes=('gecko-1-b-win2012' 'gecko-2-b-win2012' 'gecko-3-b-win2012')
key_validity="3 months"

# create (or use) a dedicated keyring (gecko-b-win)
gpg2 --no-default-keyring --keyring gecko-b-win.gpg --fingerprint

for workertype in "${workertypes[@]}"; do
folder=$(date --iso-8601 -u)_${workertype}
mkdir -p ${folder}

# create the key genertion options file (.in)
cat >${folder}/.in<<EOF
Key-Type: RSA
Key-Length: 4096
Subkey-Type: RSA
Subkey-Length: 4096
Name-Real: ${workertype}
Name-Email: noreply-${workertype}@mozilla.com
Expire-Date: $(date --iso-8601 -u -d "+${key_validity}")
%no-protection
%commit
EOF

# create the key pair
gpg2 --no-default-keyring --keyring gecko-b-win.gpg --batch --gen-key ${folder}/.in
# export the public key
gpg2 --no-default-keyring --keyring gecko-b-win.gpg --armor --export noreply-${workertype}@mozilla.com>${folder}/${workertype}.pub
done