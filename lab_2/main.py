import os

import nist_test
import json_loader


if __name__ == "__main__":
    java_seq = json_loader.load(os.path.join("lab_2", "source.json"))["java"]
    cpp_seq = json_loader.load(os.path.join("lab_2", "source.json"))["cpp"]
    print("Nist java test:")
    print(nist_test.frequency_bit_test(java_seq))
    print(nist_test.identical_consecutive_bits(java_seq))
    print(nist_test.longest_sequence_of_ones_test(java_seq))
    print("Nist cpp test:")
    print(nist_test.frequency_bit_test(cpp_seq))
    print(nist_test.identical_consecutive_bits(cpp_seq))
    print(nist_test.longest_sequence_of_ones_test(cpp_seq))