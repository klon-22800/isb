import logging

from cryptography.hazmat.primitives.serialization import (
    load_pem_public_key,
    load_pem_private_key,
)
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization


def write_symmetric_key(file_path: str, data: bytes) -> None:
    """
        The function write data to text file

    Args:
        file_path (str): path to text file
        data (bytes): data for write

    Returns:
        None
    """
    try:
        with open(file_path, "wb") as f:
            f.write(data)
    except Exception as error:
        logging.error(error)


def read_symmetric_key(file_path: str) -> bytes:
    """
        The function reads text file and return text

    Args:
        file_path (str): path to text file

    Returns:
        bytes: data from file
    """
    try:
        with open(file_path, "rb") as f:
            data = f.read()
        return data
    except Exception as error:
        logging.error(error)


def wrute_public_key(file_path:str, key: rsa.RSAPublicKey)-> None:
    try:
        with open(file_path, 'wb') as f:
            f.write(key.public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo))
    except Exception as error:
        logging.error(error)


def read_public_key(file_path: str) -> bytes:
    """
        The function reads text file and return text

    Args:
        file_path (str): path to text file

    Returns:
        bytes: data from file
    """
    try:
        with open(file_path, "rb") as f:
            data = f.read()
        return load_pem_public_key(data)
    except Exception as error:
        logging.error(error)


def write_private_key(file_path: str, key: rsa.RSAPrivateKey)-> None:
    try:
        with open(file_path, 'wb') as f:
            f.write(key.private_bytes(encoding=serialization.Encoding.PEM, format=serialization.PrivateFormat.TraditionalOpenSSL, encryption_algorithm=serialization.NoEncryption()))
    except Exception as error:
        logging.error(error)


def read_private_key(file_path: str) -> bytes:
    """
        The function reads text file and return text

    Args:
        file_path (str): path to text file

    Returns:
        bytes: data from file
    """
    try:
        with open(file_path, "rb") as f:
            data = f.read()
        return load_pem_private_key(data, password=None,)
    except Exception as error:
        logging.error(error)


def read_text(file_path: str)-> str:
    try:
        with open(file_path, "r", encoding='utf-8') as f:
            data = f.read()
        return data
    except Exception as error:
        logging.error(error)


def write_text(file_path: str, data: str)-> str:
    try:
        with open(file_path, "w", encoding='utf-8') as f:
            f.write(data)
    except Exception as error:
        logging.error(error)


def read_bytes(file_path: str)-> str:
    try:
        with open(file_path, "rb") as f:
            data = f.read()
        return data
    except Exception as error:
        logging.error(error)


def write_bytes(file_path: str, data: str)-> str:
    try:
        with open(file_path, "wb") as f:
            f.write(data)
    except Exception as error:
        logging.error(error)