import os

from cryptography.hazmat.primitives import padding as sym_padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

from serialize import Serialization


class Symmetrical:
    """Class for symmetrical algorithms"""

    def __init__(self) -> None:
        """Consructor of class with a field for serializing keys"""
        self.serialize = Serialization()

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
        text = self.serialize.read_text(text_path)

        padder = sym_padding.ANSIX923(block_size).padder()
        text = bytes(text, "UTF-8")
        padded_text = padder.update(text) + padder.finalize()

        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(symmetrical_key), modes.CBC(iv))
        encryptor = cipher.encryptor()

        c_text = iv + encryptor.update(padded_text) + encryptor.finalize()

        self.serialize.write_bytes(encrypt_text_path, c_text)
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
        text = self.serialize.read_bytes(encrypt_text_path)

        iv = text[:16]
        text = text[16:]

        cipher = Cipher(algorithms.AES(symmetric_key), modes.CBC(iv))
        decryptor = cipher.decryptor()
        dc_text = decryptor.update(text) + decryptor.finalize()
        unpadder = sym_padding.ANSIX923(block_size).unpadder()
        unpadded_dc_text = unpadder.update(dc_text) + unpadder.finalize()
        dec_text = unpadded_dc_text.decode("UTF-8")
        self.serialize.write_text(decrypt_text_path, dec_text)
        return dec_text
