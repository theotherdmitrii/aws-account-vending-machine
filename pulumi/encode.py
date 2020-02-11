import base64


def b64text(pub_key_path: str) -> str:
    """
    Encodes provided public key with base64 encoding

    :param pub_key_path:
    :return: base64 encoded public key
    """
    with open(pub_key_path, 'rb') as pub_key_file:
        return base64.b64encode(pub_key_file.read()).decode('ascii')

