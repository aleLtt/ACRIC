# Test Injectivity in the initialization vector

__DEFINITION: Injective in the Initialization Vector__

A Cyclic Redundancy Check (CRC) function F(·, ·) is said to be injective in the initialization vector if, for every fixed message M, distinct initialization vectors produce
distinct CRC values.\
Formally: F is a CRC function injective in the initialization vector if, *for all M and given initialization vectors I, I' with I ≠ I′, then F(I, M) ≠ F(I′, M)*.


We consider all CRC functions available from the [*crcmod*](https://crcmod.sourceforge.net) Python library and test their injectivity in the initialization vector.\
To do so, we fix a random message M and compute its CRC value with the available functions.\
For each function, we test over all possible initialization values and look for collisions.\
If no collision is found, the function is injective in the initialization vector; otherwise, it is not.

**N.B:** Due to 32, 64-bit CRC functions, the program will test all possible initialization vectors. In particular, if the function is injective in the initialization vector, exactly 2^32 and 2^64 values will be computed and stored, possibly leading to memory issues.\
Before running the code, either _(i)_ verify that you have enough available resources, or _(ii)_ limit the test to the bit length your system supports. 
