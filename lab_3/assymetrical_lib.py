from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding as asym_padding

from serialize import Serialization


class Asymmetrical:
    """Class for asymmetrical algorithms"""

    def __init__(self) -> None:
        """Consructor of class with a field for serializing keys"""
        self.serialize = Serialization()

    def key_generate(self) -> tuple[rsa.RSAPrivateKey, rsa.RSAPublicKey]:
        """function generate asymmetrical keys

        Returns:
            tuple[rsa.RSAPrivateKey, rsa.RSAPublicKey]: tuple of public and private keys
        """
        keys = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        return keys, keys.public_key()

    def encrypt_symmetrical_key(
        self, symmetrical_key: str, public_key_path: str, encrypted_key_path: str
    ) -> bytes:
        """function encrypt symmetric key by asymmetrical algorithm

        Args:
            symmetrical_key (str): symmetric key for encrypt
            public_key_path (str): path to public key
            encrypted_key_path (str): path to save encrypted symmetric key

        Returns:
            bytes: symmetric encrypted key
        """
        public_key = self.serialize.read_public_key(public_key_path)
        encrypted_key = public_key.encrypt(
            symmetrical_key,
            asym_padding.OAEP(
                mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )
        self.serialize.write_bytes(encrypted_key_path, encrypted_key)
        return encrypted_key

    def decrypt_symmetrical_key(
        self, encrypted_key_path: str, private_key_path: str
    ) -> bytes:
        """function decrypt encrypted symmetric key

        Args:
            encrypted_key_path (str): path to encrypted symmetric key
            private_key_path (str): path to private key

        Returns:
            bytes: decrypted symmetric key
        """
        symmetrical_key = self.serialize.read_bytes(encrypted_key_path)
        private_key = self.serialize.read_private_key(private_key_path)

        return private_key.decrypt(
            symmetrical_key,
            asym_padding.OAEP(
                mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )
