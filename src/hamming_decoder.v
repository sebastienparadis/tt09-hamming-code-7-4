/*
 * Copyright (c) 2024 Sebastien Paradis
 * SPDX-License-Identifier: Apache-2.0
 */

// Hamming Decoder
// module hamming_decoder (
//     input wire [6:0] code,            // 7-bit codeword input
//     output wire [6:0] data_out       // 7-bit corrected data output
// );

//     wire [6:0] corrected_code; // 7-bit corrected codeword
//     wire [2:0] syndrome; // Syndrome Bits

//     assign syndrome[0] = code[6] ^ code[4] ^ code[2] ^ code[0]; // S0
//     assign syndrome[1] = code[5] ^ code[4] ^ code[1] ^ code[0]; // S1
//     assign syndrome[2] = code[3] ^ code[2] ^ code[1] ^ code[0]; // S2

//     // Bit Correction
//     assign corrected_code = (syndrome != 3'b000) ? (code ^ (1 << (7 - syndrome))) : code;

//     assign data_out = corrected_code;
// endmodule



// Hamming Decoder
module hamming_decoder (
    input wire [6:0] code,         // 7-bit codeword input
    output wire [7:0] data_out     // 8-bit output (MSB indicates error status)
);

    wire [6:0] corrected_code;     // 7-bit corrected codeword
    wire [2:0] syndrome;           // Syndrome bits
    wire overall_parity;           // Overall parity check
    wire single_bit_error;         // Single-bit error flag
    wire two_bit_error;            // Two-bit error flag

    // Calculate syndrome bits
    assign syndrome[0] = code[6] ^ code[4] ^ code[2] ^ code[0]; // S0
    assign syndrome[1] = code[5] ^ code[4] ^ code[1] ^ code[0]; // S1
    assign syndrome[2] = code[3] ^ code[2] ^ code[1] ^ code[0]; // S2

    // Calculate overall parity of the codeword (all bits XORed together)
    assign overall_parity = code[6] ^ code[5] ^ code[4] ^ code[3] ^ code[2] ^ code[1] ^ code[0];

    // Determine if there is a single-bit error
    assign single_bit_error = (syndrome != 3'b000);

    // Determine if there is a two-bit error (when syndrome is non-zero and overall parity fails)
    assign two_bit_error = single_bit_error && overall_parity;

    // Perform bit correction if single-bit error detected
    assign corrected_code = single_bit_error ? (code ^ (1 << (7 - syndrome))) : code;

    // Set the MSB of the output to 1 for two-bit errors, otherwise 0
    assign data_out = two_bit_error ? {1'b1, code} : {1'b0, corrected_code};

endmodule
