# PYTHON SCRIPT TO CHECK THE LINEARITY PROPERTY OF CRC FUNCTIONS AVAILABLE FROM THE crcmod LIBRARY

# For ACRIC better security, it is desirable that CRC functions are not linear
# We first check the linearity property of CRC functions in their standard definition
# Then, we check the linearity property of CRC functions using an initialization vector different from the standard one, as expected by ACRIC.

# !!!! Before running the script, ensure you have the crcmod library correctly installed in your system

import random
import crcmod.predefined

random.seed(42)

# List all CRC algorithms in the library
ALGOS = [
        "crc-8", "crc-8-darc", "crc-8-i-code", "crc-8-itu", "crc-8-maxim", "crc-8-rohc", "crc-8-wcdma",
        "crc-16", "crc-16-buypass", "crc-16-dds-110", "crc-16-dect", "crc-16-dnp", "crc-16-en-13757", "crc-16-genibus",
        "crc-16-maxim", "crc-16-mcrf4xx", "crc-16-riello", "crc-16-t10-dif", "crc-16-teledisk", "crc-16-usb",
        "x-25", "xmodem", "modbus", "kermit", "crc-ccitt-false", "crc-aug-ccitt",
        "crc-24", "crc-24-flexray-a", "crc-24-flexray-b",
        "crc-32", "crc-32-bzip2", "crc-32c", "crc-32d", "crc-32-mpeg", "posix", "crc-32q",
        "jamcrc", "xfer", "crc-64", "crc-64-we", "crc-64-jones"
]


def test_linearity_standard(crc_func, message_length=16, trials=1000):
    """
    Checks if given crc function is linear.
    That is, for random M1, M2: crc(M1) XOR crc(M2) == crc(M1 XOR M2)
    Returns True if all tests pass, False otherwise.
    """
    
    for _ in range(trials):
        # Generate two random messages (bytes)
        M1 = bytes(random.getrandbits(8) for _ in range(message_length))
        M2 = bytes(random.getrandbits(8) for _ in range(message_length))

        crc1 = crc_func(M1)
        crc2 = crc_func(M2)

        # XOR the two messages
        Mx = bytes(a ^ b for a, b in zip(M1, M2))
        crc_x = crc_func(Mx)

        if (crc1 ^ crc2) != crc_x:
            return False
    return True


def test_linearity_custom(crc_func, custom_init, message_length=16, trials=10000):
    """
    Checks if, for random byte-strings M1, M2:
        crc_func(M1, custom_init) XOR crc_func(M2, custom_init) == crc_func(M1 XOR M2, custom_init).
    Returns True if it holds for all trials, False otherwise.
    """

    init_value = custom_init

    for _ in range(trials):
        M1 = bytes(random.getrandbits(8) for _ in range(message_length))
        M2 = bytes(random.getrandbits(8) for _ in range(message_length))

        crc1 = crc_func(M1, custom_init)
        crc2 = crc_func(M2, custom_init)


        Mx   = bytes(a ^ b for a, b in zip(M1, M2))
        crcx = crc_func(Mx, custom_init)

        if (crc1 ^ crc2) != crcx:
            return False
    return True





linear_functions_std = []
linear_functions_custom = []

for algo in ALGOS:
    try:
        crc_func = crcmod.predefined.mkPredefinedCrcFun(algo)
    except KeyError:
        print(f"{algo:25s} => Not supported in this version of crcmod")
        continue

    is_linear = test_linearity_standard(crc_func)

    if is_linear:
        linear_functions_std.append(algo)


    # Uncomment if you want to see the result for each algorithm
    #print(f"{algo:25s} => {'Linear' if is_linear else 'Non-linear'}")



# Custom initialization vector -> set to be as large as the largest CRC value in the library.
# The function will naturally discard higher bits, or you can manually mask them.
CUSTOM_INIT = 0x1234567890123456

for algo in ALGOS:

    try:
        # Build the standard CRC function from crcmod.predefined
        base_func = crcmod.predefined.mkPredefinedCrcFun(algo)

    except KeyError:
        # Some older versions of crcmod may not have all these definitions:
        print(f"{algo:24s} => Not available in this version of crcmod")
        continue


    # Test linearity with a custom initial CRC value
    is_linear = test_linearity_custom(base_func, custom_init=CUSTOM_INIT)

    if is_linear:
        linear_functions_custom.append(algo)


    # Uncomment if you want to see the result for each algorithm
    #print(f"{algo:24s} => {'Linear' if is_linear else 'Non-linear'} " f"(custom init = 0x{CUSTOM_INIT:X})")


# Comparison of results standarc vs custom initialization vector
print()
print("STANDARD - Linear functions:")
print(linear_functions_std)
print()
print("CUSTOM - Linear functions:")
print(linear_functions_custom)
