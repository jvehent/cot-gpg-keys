Public GPG keys for generic-worker go here.

To create new keys for Windows worker types:

- edit generate_keys.sh (to add or remove worker types)
- run the key generation script
- create or edit secrets at: https://tools.taskcluster.net/secrets/.
  for each worker type with a new key:
  - export the private key with a command like:
    ```bash
    gpg2 --no-default-keyring --keyring gecko-b-win.gpg --armor --export-secret-key noreply-<worker type>@mozilla.com
    ```
  - create or edit the secret named: ```repo:github.com/mozilla-releng/OpenCloudConfig:cot-<worker type>```.
  - the contents of the secret should be in json format as below (replace newlines with "\n"):
  
    ```json
    {
      "cot_private_key": "-----BEGIN PGP PRIVATE KEY BLOCK-----\nVersion: GnuPG v2\n\nsecret removed\n-----END PGP PRIVATE KEY BLOCK-----"
    }
    ```
- commit and push new public keys to this repo
