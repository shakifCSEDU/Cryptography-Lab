# For Encryption --- > python main.py input/audio.wav output/encrypt_audio.wav
# For Decryption ----> python main.py output/encrypt_audio.wav output/decrypt_audio.wav
import sys

from BitVector import *
def generate_state_vector(key_ascii):
    key_length = len(key_ascii)
    key = []

    #Here We encode the ascii value for every character
    for val in key_ascii:
        key.append(ord(val))

    S = [0]*256 # State Vector
    T = [0]*256 # Temporary Vector
    # Initialization
    for i in range(256):
        S[i] = i
        T[i] = key[i % key_length]

    # Initial Permutation
    j = 0
    for i in range(256):
        j = (j + S[i] + T[i]) % 256
        S[i], S[j] = S[j], S[i]

    return S

def stream_cipher(input_bit_vector,S,output_file):
    total_bits = len(input_bit_vector)
    block_index = 0
    bit_index = 0

    i, j = 0, 0
    while bit_index < total_bits:

        # key stream
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        t = (S[i] + S[j]) % 256
        k = S[t]
        k_bv = BitVector(intVal=k, size=8)

        # input block
        block_bv = input_bit_vector[bit_index:bit_index + 8]
        block_index += 1
        bit_index += 8

        # encryption/decryption
        output_bv = block_bv ^ k_bv

        # output
        output_bv.write_to_file(output_file)


if __name__ == '__main__':
    # Command Line input and Output path set.
    input_path = sys.argv[1]
    output_path = sys.argv[2]

    # Key from console
    #The key must be 16characters long.
    key = input("Enter a key : ")

    with open(input_path,"rb") as input_file:
        header_data = input_file.read(44)
        raw_data = input_file.read()
        input_bit_vector = BitVector(rawbytes =raw_data)

    output_file = open(output_path,"wb")
    output_file.write(header_data)

    #Here We apply the RC4 algorithm
    S = generate_state_vector(key)
    stream_cipher(input_bit_vector,S,output_file)


