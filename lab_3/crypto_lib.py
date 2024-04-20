import os

import serialize

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import padding as sym_padding
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding as asym_padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


class Symmetrical:
    """Class for symmetrical algorithms"""

    def key_generate(self, size: int) -> bytes:
        """function generate symmetrical key

        Args:
            size (int): len of key in bytes

        Returns:
            bytes: pseudo-random generatd symmetrical key
        """
        return os.urandom(size)

    def encrypt_text(
        self,
        text_path: str,
        symmetrical_key: str,
        encrypt_text_path: str,
        block_size: int,
    ) -> str:
        """function encrypt text by symmetrical key

        Args:
            text_path (str): path to text for encryption
            symmetrical_key (str): symmetrical key for encryption
            encrypt_text_path (str): path to save encrypted key
            block_size (int): len of symmetrical key in bytes

        Returns:
            str: encrypted text
        """
        text = serialize.read_text(text_path)

        padder = sym_padding.ANSIX923(block_size).padder()
        text = bytes(text, "UTF-8")
        padded_text = padder.update(text) + padder.finalize()

        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(symmetrical_key), modes.CBC(iv))
        encryptor = cipher.encryptor()

        c_text = iv + encryptor.update(padded_text) + encryptor.finalize()

        serialize.write_bytes(encrypt_text_path, c_text)
        return c_text

    def decrypt_text(
        self,
        symmetric_key: str,
        encrypt_text_path: str,
        decrypt_text_path: str,
        block_size,
    ) -> str:
        """function decrypt text by symmetrical key

        Args:
            symmetric_key (str): symmetrical key for encryption
            encrypt_text_path (str): path to encrypted text
            decrypt_text_path (str): path to save decrypted text
            block_size (_type_): len of symmetrical key in bytes

        Returns:
            str: decrypted text
        """
        text = serialize.read_bytes(encrypt_text_path)

        iv = text[:16]
        text = text[16:]

        cipher = Cipher(algorithms.AES(symmetric_key), modes.CBC(iv))
        decryptor = cipher.decryptor()
        dc_text = decryptor.update(text) + decryptor.finalize()
        unpadder = sym_padding.ANSIX923(block_size).unpadder()
        unpadded_dc_text = unpadder.update(dc_text) + unpadder.finalize()
        dec_text = unpadded_dc_text.decode("UTF-8")
        serialize.write_text(decrypt_text_path, dec_text)
        return dec_text


class Asymmetrical:
    """Class for asymmetrical algorithms"""

    def key_generate(self) -> tuple[rsa.RSAPublicKey, rsa.RSAPrivateKey]:
        """function generate asymmetrical keys

        Returns:
            tuple[rsa.RSAPublicKey, rsa.RSAPrivateKey]: tuple of public and private keys
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
        public_key = serialize.read_public_key(public_key_path)
        encrypted_key = public_key.encrypt(
            symmetrical_key,
            asym_padding.OAEP(
                mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )
        serialize.write_bytes(encrypted_key_path, encrypted_key)
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
        symmetrical_key = serialize.read_bytes(encrypted_key_path)
        private_key = serialize.read_private_key(private_key_path)

        return private_key.decrypt(
            symmetrical_key,
            asym_padding.OAEP(
                mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )
