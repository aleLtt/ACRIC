# Test Integrity Protection

The script empirically estimates ACRIC's integrity protection guarantees against a tampering attack: given a legitimate message M with its corresponding ACRIC value, the attacker aims at modifying M into M' without altering the ACRIC value and being undetected.\
This corresponds to a CRC collision scenario in which two different messages M, M' have the same CRC value (using the same initialization vector).\
For each message M, we tested 100.000.000 other different messages M'.\
For each CRC function, experiments are run testing 10 legitimate messages M.\
We thus empirically estimate the attack success probability as the number of collisions over all tests done.

Results show that the attack success probability is negligible, and it gets lower and lower as the CRC bit length increases.
This experimentally demonstrates ACRIC's security and integrity protection guarantees.
