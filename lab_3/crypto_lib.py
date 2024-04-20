import os

import serialize


from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import padding as sym_padding
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding as asym_padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


class Symmetrical:
    """write latter"""

    def key_generate(self, size: int):
        return os.urandom(size)

    def encrypt_text(
        self,
        text_path: str,
        symmetrical_key: str,
        encrypt_text_path: str,
        block_size: int,
    ) -> str:
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
    """write latter"""

    def key_generate(self) -> tuple[rsa.RSAPublicKey, rsa.RSAPrivateKey]:
        keys = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        return keys, keys.public_key()
    

    def encrypt_symmetrical_key(self, symmetrical_key: str, public_key_path: str, encrypted_key_path: str):
        public_key = serialize.read_public_key(public_key_path)
        encrypted_key = public_key.encrypt(symmetrical_key, asym_padding.OAEP(mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),algorithm=hashes.SHA256(),label=None))

        serialize.write_bytes(encrypted_key_path, encrypted_key)
        return encrypted_key

    def decrypt_symmetrical_key(self, encrypted_key_path: str, private_key_path:str):
        symmetrical_key = serialize.read_symmetric_key(encrypted_key_path)
        print(symmetrical_key)
        private_key = serialize.read_private_key(private_key_path)

        return private_key.decrypt(symmetrical_key, asym_padding.OAEP(mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),algorithm=hashes.SHA256(),label=None))

a = Symmetrical()
symm_key = a.key_generate(32)
a.encrypt_text("lab_3//tests//text.txt", symm_key, "lab_3//tests//encr.txt", 256)
a.decrypt_text(symm_key, "lab_3//tests//encr.txt", "lab_3//tests//decr.txt", 256)
b = Asymmetrical()
keys = b.key_generate()
serialize.write_private_key('lab_3//tests//private_key.pem',keys[0])
serialize.wrute_public_key('lab_3//tests//public_key.pem',keys[1])
b.encrypt_symmetrical_key(symm_key, 'lab_3//tests//public_key.pem', 'lab_3//tests//encr_symmetric_key.txt')
new_symm = b.decrypt_symmetrical_key('lab_3//tests//encr_symmetric_key.txt', 'lab_3//tests//private_key.pem')
