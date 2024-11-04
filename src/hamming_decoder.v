/*
 * Copyright (c) 2024 Sebastien Paradis
 * SPDX-License-Identifier: Apache-2.0
 */

// Hamming Decoder
module hamming_decoder (
    input wire [6:0] code,            // 7-bit codeword input
    output wire [6:0] data_out       // 7-bit corrected data output
);

    wire [6:0] corrected_code; // 7-bit corrected codeword
    wire [2:0] syndrome; // Syndrome Bits

    assign syndrome[0] = code[6] ^ code[4] ^ code[2] ^ code[0]; // S0
    assign syndrome[1] = code[5] ^ code[4] ^ code[1] ^ code[0]; // S1
    assign syndrome[2] = code[3] ^ code[2] ^ code[1] ^ code[0]; // S2

    // Bit Correction
    assign corrected_code = (syndrome != 3'b000) ? (code ^ (1 << (7 - syndrome))) : code;

    assign data_out = corrected_code;
endmodule
