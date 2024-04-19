import os

import serialize 


from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes



class Symmetrical:
    """write latter
    """
    def key_generate(self, size: int):
        return os.urandom(size)
    
    def encrypt_text(self, file_path:str, symmetrical_key_path:str, encrypt_text_path:str, block_size: int)->str:
        text = serialize.read_text(file_path)

        padder = padding.ANSIX923(block_size).padder()
        text = bytes(text, 'UTF-8')
        padded_text = padder.update(text)+padder.finalize()

        iv = os.urandom(16)
        key = serialize.read_symmetric_key(symmetrical_key_path)
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
        encryptor = cipher.encryptor()

        c_text = iv + encryptor.update(padded_text) + encryptor.finalize()

        serialize.write_bytes(encrypt_text_path, c_text)
        return c_text

    def decrypt_text(self, symmetrical_key_path:str, encrypt_text_path: str, decrypt_text_path:str, block_size)->str:
        text = serialize.read_bytes(encrypt_text_path)

        iv = text[:16]
        text = text[16:]
        symmetric_key = serialize.read_symmetric_key(symmetrical_key_path)
        cipher = Cipher(algorithms.AES(symmetric_key), modes.CBC(iv))
        decryptor = cipher.decryptor()
        dc_text = decryptor.update(text) + decryptor.finalize()
        unpadder = padding.ANSIX923(block_size).unpadder()
        unpadded_dc_text = unpadder.update(dc_text) + unpadder.finalize()
        dec_text = unpadded_dc_text.decode('UTF-8')
        serialize.write_text(decrypt_text_path, dec_text)
        return

a = Symmetrical()
serialize.write_symmetric_key('lab_3//tests//symmetric_key.txt', a.key_generate(32))
a.encrypt_text("lab_3//tests//text.txt", "lab_3//tests//symmetric_key.txt", "lab_3//tests//encr.txt", 128)
a.decrypt_text("lab_3//tests//symmetric_key.txt", "lab_3//tests//encr.txt", "lab_3//tests//decr.txt", 128)
