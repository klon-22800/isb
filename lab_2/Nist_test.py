import math
import logging

import mpmath

from const import PI


def frequency_bit_test(sequence: str) -> float:
    """frequency bit test

    Args:
        sequence (str): pseudorandom sequence of 1 and 0

    Returns:
        float: P-value
    """
    try:
        length = len(sequence)
        if length > 0:
            sum = 0
            for bit in sequence:
                if int(bit):
                    sum -= 1
                else:
                    sum += 1
            s = math.fabs(sum) / (length**0.5)
            return math.erfc(s / (2**0.5))
    except Exception as error:
        logging.error(error)


def identical_consecutive_bits(sequence: str) -> float:
    """identical consecutive bits test

    Args:
        sequence (str): pseudorandom sequence of 1 and 0

    Returns:
        float: P-value
    """
    try:
        length = len(sequence)
        if length > 0:
            ones_per = sequence.count("1") / length
            if abs(ones_per - 0.5) < (2 / (length**0.5)):
                v_n = 0
                for i in range(length - 1):
                    if sequence[i] != sequence[i + 1]:
                        v_n += 1
                return (abs(v_n - 2 * length * ones_per * (1 - ones_per))) / (
                    2 * (2 * length) ** 0.5 * ones_per * (1 - ones_per)
                )
            else:
                return 0
        else:
            return 0
    except Exception as error:
        logging.error(error)


def longest_sequence_of_ones_test(sequence: str) -> float:
    """longest sequence of ones test

    Args:
        sequence (str): pseudorandom sequence of 1 and 0

    Returns:
        float: P-value
    """
    try:
        length = len(sequence)
        if length > 0:
            block_len_count = {1: 0, 2: 0, 3: 0, 4: 0}
            for i in range(0, length, 8):
                block = sequence[i : i + 8]
                block_len = longest_sequence(block, "1")
                if block_len >= 4:
                    block_len_count[4] += 1
                elif block_len <= 1:
                    block_len_count[1] += 1
                else:
                    block_len_count[block_len] += 1
            xi_square = 0
            for i in range(1, 4):
                xi_square += ((block_len_count[i + 1] - 16 * PI[i]) ** 2) / (16 * PI[i])
            return mpmath.gammainc(3 / 2, xi_square / 2)
        else:
            return 0
    except Exception as error:
        logging.error(error)


def longest_sequence(string: str, symb: str) -> int:
    """Counts the longest sequence of symbols

    Args:
        string (str): sequence of symbols
        symb (str): symbol that we count

    Returns:
        int: length of the longest sequence
    """
    try:
        count = 1
        max = 0
        for i in range(1, len(string)):
            if string[i] == string[i - 1] == symb:
                count += 1
                if count > max:
                    max = count
            else:
                count = 1
        return max
    except Exception as error:
        logging.error(error)