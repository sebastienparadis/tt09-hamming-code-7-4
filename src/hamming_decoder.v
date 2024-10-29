/*
 * Copyright (c) 2024 Sebastien Paradis
 * SPDX-License-Identifier: Apache-2.0
 */

// Hamming Decoder
module hamming_decoder (
    input wire [6:0] code,            // 7-bit codeword input
    output wire [6:0] data_out,       // 7-bit corrected data output
    input wire rst_n                  // Active-low reset signal
);

    // Error detection and correction
    output wire [6:0] corrected_code; // 7-bit corrected codeword
    wire [2:0] syndrome; // Parity check bits

    assign syndrome[0] = code[6] ^ code[4] ^ code[2] ^ code[0]; // S3
    assign syndrome[1] = code[5] ^ code[4] ^ code[1] ^ code[0]; // S2
    assign syndrome[2] = code[3] ^ code[2] ^ code[1] ^ code[0]; // S1

    // Syndrome and Bit Correction
    assign corrected_code = (rst_n) ? (
        (syndrome != 3'b000) ? (code ^ (1 << (7 - syndrome))) : code
    ) : 7'b0;
    // end

    assign data_out = corrected_code;
endmodule