import base64
from typing import Any

import gnupg


class PasswordDecryptor:
    gpg: gnupg.GPG
    """
    """

    email: str
    """
    """

    passphrase: str
    """
    """

    key: Any
    """
    """

    public_key: Any
    """
    """

    def __init__(self, email: str, passphrase: str):
        self.gpg = gnupg.GPG()
        self.email = email
        self.passphrase = passphrase
        input_data = self.gpg.gen_key_input(
            name_email=email,
            passphrase=passphrase)
        self.key = self.gpg.gen_key(input_data)
        self.public_key = self.gpg.export_keys(str(self.key), armor=False)

    # def export(self) -> str:
    #     return base64.b64encode(self.public_key.encode('ascii')).decode('ascii')

    def export(self) -> str:
        return base64.standard_b64encode(self.public_key).decode('ascii')

    def decrypt(self, message: str) -> str:
        b64decoded = base64.b64decode(message)
        return str(self.gpg.decrypt(b64decoded, passphrase=self.passphrase))


if __name__ == "__main__":
    decryptor = PasswordDecryptor("dtcimbal@gmail.com", "hain6Izo")
    # print(decryptor.gpg.list_keys())
    # print(decryptor.key)
    print(decryptor.export())
