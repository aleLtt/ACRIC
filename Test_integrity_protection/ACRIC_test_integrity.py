# PYTHON SCRIPT TO EXPERIMENTALLY EVALUATE ACRIC'S INTEGRTY PROTECTION (TAMPERING RESISTANCE) PROPERTY USING THE crcmod LIBRARY

# We first select a random message considered as the legitimate message and compute the corresponding CRC value using a custom initialization vector
# Then, we generate another random message and compute its CRC value using the same initialization vector
# We check it the two CRC values are the same or not
# we repeat this operation several times for all algorithms available in the library

# !!!! Before running the script, ensure you have the crcmod library correctly installed in your system


import random
import crcmod.predefined

random.seed(42)

def generate_random_message(min_length=1, max_length=250):

    """Generate a random bytes message of a random length between min_length and max_length."""
    length = random.randint(min_length, max_length)
    return bytearray(random.getrandbits(8) for _ in range(length))


print("ACRIC - Test of CRC message collision probability\n")

# Set number of iterations.
N_prime_tests = 100_000_000         # number of messages to test for collision
n_rounds = 10                        # number of test for each algorithm

# Disctionary of all possible algorithms in the library and corresponding CRC lengths
algs = {
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

# Process each CRC algorithm
for algo in algs:

    collision_counter = 0

    for k in range(n_rounds):

        # Generate a random initialization value: any value in 0 <= init < (1 << length)
        init_value = random.randint(0, (1 << algs[algo]) - 1)

        try:
            # Build the standard CRC function from crcmod.predefined
            crc_func = crcmod.predefined.mkPredefinedCrcFun(algo)

        except KeyError:
            # Some older versions of crcmod may not have all these definitions:
            print(f"{algo:24s} => Not available in this version of crcmod")
            continue

        # Generate a random message M of length between 1 and 250 bytes and compute its CRC.
        M = generate_random_message(1, 50)
        crc_M = crc_func(M, init_value)

        # Generate M' and check CRC values.
        for i in range(N_prime_tests):

            M_prime = generate_random_message(1, 250)
            
            # Ensure that the generated M_prime is different from M
            while M_prime == M:
                M_prime = generate_random_message(1, 250)

            crc_M_prime = crc_func(M_prime, init_value)

            # Check for CRC collision
            if crc_M_prime == crc_M:
                collision_counter += 1


    print(f"{algo} - ", end="")
    print(f"Collision prob: {collision_counter / (n_rounds * N_prime_tests):.10f}")
