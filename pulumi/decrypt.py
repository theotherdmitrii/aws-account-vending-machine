import base64

import gnupg


class PasswordDecryptor:

    def __init__(self, armored_key_path: str):
        self.gpg = gnupg.GPG()
        self.gpg.import_keys(armored_key_path)

    def decrypt(self, message: str, passphrase: str) -> str:
        b64decoded = base64.b64decode(message)
        return str(self.gpg.decrypt(b64decoded, passphrase=passphrase))
