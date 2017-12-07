#!/bin/bash

# add or remove worker types here
#workertypes=('gecko-1-b-win2012' 'gecko-2-b-win2012' 'gecko-3-b-win2012')
workertypes=('gecko-3-b-win2012')
key_validity="4 months"
key_valid_start=$(date --iso-8601 -u)
key_valid_end=$(date --iso-8601 -u -d "+${key_validity}")
keyring=${key_valid_start}_${key_valid_end}_gecko-b-win.gpg

# create (or use) a dedicated keyring (${key_valid_start}_${key_valid_end}_gecko-b-win)
gpg2 --export-ownertrust > ~/.gnupg/ownertrust-gpg.txt
gpg2 --no-default-keyring --keyring ${keyring} --fingerprint
gpg2 --no-default-keyring --keyring ${keyring} --import-ownertrust ~/.gnupg/ownertrust-gpg.txt

for workertype in "${workertypes[@]}"; do
folder=${key_valid_start}_${key_valid_end}_${workertype}
mkdir -p ${folder}

# create the key genertion options file (.in)
cat >${folder}/.in<<EOF
Key-Type: RSA
Key-Length: 4096
Subkey-Type: RSA
Subkey-Length: 4096
Name-Real: ${workertype}
Name-Email: noreply-${workertype}@mozilla.com
Expire-Date: ${key_valid_end}
%no-protection
%commit
EOF

# create the key pair
gpg2 --no-default-keyring --keyring ${keyring} --batch --gen-key ${folder}/.in
# export the public key
gpg2 --no-default-keyring --keyring ${keyring} --armor --export noreply-${workertype}@mozilla.com>${folder}/${workertype}.pub
done