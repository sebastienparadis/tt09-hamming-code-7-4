<!---

This file is used to generate your project datasheet. Please fill in the information below and delete any unused
sections.

You can also include images in this folder and reference them in the markdown. Each image must be less than
512 kb in size, and the combined size of all images must be less than 1 MB.
-->

## How it works

### Hamming Encoder (7,4) Overview
The Hamming (7,4) encoder is a linear error-correcting code that encodes 4 data bits into 7 bits by adding 3 parity bits, which can detect and correct a single-bit error. 

#### Details
-   Parity: p1 p2 p3
-   Data: d1 d2 d3 d4
- 	Input: 4 data bits (d1 d2 d3 d4)
-	Output: 7 encoded bits (p1 p2 d1 p3 d2 d3 d4)

#### Parity Bit Calculations
1.	p1 covers bits d1, d2, and d4.
	- p1 = d1 XOR d2 XOR d4
2.	p2 covers bits d1, d3, and d4.
	- p2 = d1 XOR d3 XOR d4
3.	p3 covers bits d2, d3, and d4.
    - p3 = d2 XOR d3 XOR d4

#### Encoder Output Format
** p1, p2, d1, p3, d2, d3, d4 **

### Hamming Decoder (7,4) Overview
The decoder checks the received 7-bit word for errors and corrects a single-bit error if detected. The process involves recalculating the parity bits and comparing them with the received parity.

#### Syndrome Calculation
The syndrome indicates the position of an error (if any):
1. S0 is recalculated using the same bits used to calculate p1 during encoding:
	- S0 = p1' XOR d1 XOR d2 XOR d4
2. S1 recalculates p2:
    - S1 = p2' XOR d1 XOR d3 XOR d4
3. S2 recalculates p3:
    - S2 = p3' XOR d2 XOR d3 XOR d4

#### Error Correction
The syndrome {S2, S1, S0} gives the error location:
- If the syndrome is 000, no error is detected.
- If the syndrome is non-zero, the position of the error corresponds to the syndrome value (1 for the least significant bit, 7 for the most significant bit).
- E.g. if syndrome is 010, then. Our error bit is at bit 4
- If an error is detected, flip the bit at the position indicated by the syndrome.

## How to test

Explain how to use your project

### TODO

## External hardware

List external hardware used in your project (e.g. PMOD, LED display, etc), if any

### TODO
