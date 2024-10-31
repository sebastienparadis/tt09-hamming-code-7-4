/*
 * Copyright (c) 2024 Sebastien Paradis
 * SPDX-License-Identifier: Apache-2.0
 */


// Hamming Encoder
module hamming_encoder (
    input wire [3:0] data,   // 4 data bits
    output wire [6:0] code   // 7-bit codeword
);

    wire p1, p2, p3;

    //data: d1 d2 d3 d4
    //parity: p1 p2 p3

    assign p1 = data[3] ^ data[2] ^ data[0]; // p1 is the parity bit for bits 1, 2, and 4
    assign p2 = data[3] ^ data[1] ^ data[0]; // p2 is the parity bit for bits 1, 3, and 4
    assign p3 = data[2] ^ data[1] ^ data[0]; // p3 is the parity bit for bits 2, 3, and 4

    assign code = {p1, p2, data[3], p3, data[2], data[1], data[0]}; // p1 p2 d1 p3 d2 d3 d4
endmodule