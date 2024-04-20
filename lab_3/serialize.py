import logging

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import (
    load_pem_public_key,
    load_pem_private_key,
)


def wrute_public_key(file_path: str, key: rsa.RSAPublicKey) -> None:
    """function write public file in .pem file

    Args:
        file_path (str): path to .pem file
        key (rsa.RSAPublicKey): public key to write
    """
    try:
        with open(file_path, "wb") as f:
            f.write(
                key.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo,
                )
            )
    except Exception as error:
        logging.error(error)


def read_public_key(file_path: str) -> rsa.RSAPublicKey:
    """
        The function reads .pem file and return public key

    Args:
        file_path (str): path to .pem file

    Returns:
        rsa.RSAPublicKey: public key from file
    """
    try:
        with open(file_path, "rb") as f:
            data = f.read()
        return load_pem_public_key(data)
    except Exception as error:
        logging.error(error)


def write_private_key(file_path: str, key: rsa.RSAPrivateKey) -> None:
    """function write private key to .pem file

    Args:
        file_path (str): path to .pem file
        key (rsa.RSAPrivateKey): private key to write
    """
    try:
        with open(file_path, "wb") as f:
            f.write(
                key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.TraditionalOpenSSL,
                    encryption_algorithm=serialization.NoEncryption(),
                )
            )
    except Exception as error:
        logging.error(error)


def read_private_key(file_path: str) -> rsa.RSAPrivateKey:
    """
        The function reads private key from .pem file

    Args:
        file_path (str): path to .pem file

    Returns:
        rsa.RSAPrivateKey: private key from file
    """
    try:
        with open(file_path, "rb") as f:
            data = f.read()
        return load_pem_private_key(
            data,
            password=None,
        )
    except Exception as error:
        logging.error(error)


def read_text(file_path: str) -> str:
    """function read text from file

    Args:
        file_path (str): path to file for read

    Returns:
        str: text from file
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = f.read()
        return data
    except Exception as error:
        logging.error(error)


def write_text(file_path: str, data: str) -> None:
    """function write text to file

    Args:
        file_path (str): path to file for write
        data (str): data to write
    """
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(data)
    except Exception as error:
        logging.error(error)


def read_bytes(file_path: str) -> str:
    """function read bytes from txt file

    Args:
        file_path (str): path to file for read

    Returns:
        str: data from file
    """
    try:
        with open(file_path, "rb") as f:
            data = f.read()
        return data
    except Exception as error:
        logging.error(error)


def write_bytes(file_path: str, data: str) -> None:
    """function write bytes to txt file

    Args:
        file_path (str): path to file for write
        data (str): data to write
    """
    try:
        with open(file_path, "wb") as f:
            f.write(data)
    except Exception as error:
        logging.error(error)
