# PYTHON SCRIPT TO EXPERIMENTALLY EVALUATE WHICH CRC FUNCTIONS PROVIDED IN THE crcmod LIBRARY ARE INJECTIVE IN THE INITIALIZATION VECTOR

# We first fix a random message
# Given a CRC function, we test all possible initialization vectors to compute the CRC value
# Computed values are saved in a set object
# We then check whether there is any CRC collision -> two different initialization vectors lead to the same CRC value 
# We repeat the procedure for all available functions

# !!!! Before running the script, ensure you have the crcmod library correctly installed on your system

import random
import crcmod.predefined

random.seed(42)

# Dictionary of all algorithms in crcmod library with corresponding CRC lengths
ALGOS = {
    "crc-8": 8,
    "crc-8-darc": 8,
    "crc-8-i-code": 8,
    "crc-8-itu": 8,
    "crc-8-maxim": 8,
    "crc-8-rohc": 8,
    "crc-8-wcdma": 8,

    "crc-16": 16,
    "crc-16-buypass": 16,
    "crc-16-dds-110": 16,
    "crc-16-dect": 16,
    "crc-16-dnp": 16,
    "crc-16-en-13757": 16,
    "crc-16-genibus": 16,
    "crc-16-maxim": 16,
    "crc-16-mcrf4xx": 16,
    "crc-16-riello": 16,
    "crc-16-t10-dif": 16,
    "crc-16-teledisk": 16,
    "crc-16-usb": 16,
    "x-25": 16,
    "xmodem": 16,
    "modbus": 16,
    "kermit": 16,
    "crc-ccitt-false": 16,
    "crc-aug-ccitt": 16,

    "crc-24": 24,
    "crc-24-flexray-a": 24,
    "crc-24-flexray-b": 24,

    "crc-32": 32,
    "crc-32-bzip2": 32,
    "crc-32c": 32,
    "crc-32d": 32,
    "crc-32-mpeg": 32,
    "posix": 32,
    "crc-32q": 32,
    "jamcrc": 32,
    "xfer": 32,

    "crc-64": 64,
    "crc-64-we": 64,
    "crc-64-jones": 64,
}

# Pick a random message of some length in bytes. For example, we pick 4 bytes, i.e. 32 bits of random data:
random_message_length = 4
random_msg = random.getrandbits(random_message_length * 8).to_bytes(random_message_length, 'big')

# Just to visualize the random message we selected:
msg_hex = random_msg.hex().upper()
print(f"Random message (hex) = {msg_hex}\n")

for crc_name in ALGOS:
    bit_width = ALGOS[crc_name]

    # Generate the CRC function for this algorithm.
    crc_func = crcmod.predefined.mkPredefinedCrcFun(crc_name)

    # Enumerate all possible IVs for that bit width: [0..2^bit_width - 1]
    max_iv = (1 << bit_width) - 1

    # For each IV, compute the CRC of the single random message
    seen = set()
    collision_found = False

    for iv in range(max_iv + 1):
        crc_val = crc_func(random_msg, crc=iv)
        if crc_val in seen:
            # 5) If there's a repeated CRC value, we found a collision
            collision_found = True
            break
        seen.add(crc_val)

    # Print result
    if collision_found:
        print(f"{crc_name:25s} : collisions found among all IVs ({bit_width}-bit)!")
    else:
        print(f"{crc_name:25s} : NO collisions among all IVs ({bit_width}-bit).")
