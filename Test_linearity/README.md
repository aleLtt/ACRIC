# Test Linearity

The script checks if and which CRC functions from the *crcmos* Python librarty are linear functions such that: _F(x) XOR F(y) = F(x XOR Y)_.\
We run the linearity test for two cases: _(i)_ standard CRC function definitions, and _(ii)_ CRC functions with custom initialization vector.

Experimental results show that all the CRC functions that, in their standard definition, use a null initialization vector (IV = 0x00) and do not perform XOR to the output (XOR-out = 0), are linear.\
However, changing the initialization vector makes these functions non-linear. This shows that leveraging a custom initialization vector for ACRIC computation removes the linearity property of some CRC functions, thus further increasing security.
