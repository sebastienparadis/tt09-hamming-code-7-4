/*
 * Copyright (c) 2024 Sebastien Paradis
 * SPDX-License-Identifier: Apache-2.0
 */

`default_nettype none

// Top Module
module tt_um_sebastienparadis_hamming_top (
    input  wire [7:0] ui_in,    // Dedicated inputs
    output wire [7:0] uo_out,   // Dedicated outputs
    input  wire [7:0] uio_in,   // IOs: Input path
    output wire [7:0] uio_out,  // IOs: Output path
    output wire [7:0] uio_oe,   // IOs: Enable path (active high: 0=input, 1=output)
    input  wire       ena,      // always 1 when the design is powered, so you can ignore it
    input  wire       clk,      // clock
    input  wire       rst_n     // reset_n - low to reset
);

    // Mode selection
    wire mode = ui_in[7];            // MSB of ui_in as mode selector (0 => Encode, 1 => Decode)

    // Input signals
    wire [3:0] data_in = ui_in[3:0]; // 4-bit data for encoding mode
    wire [6:0] code_in = ui_in[6:0]; // 7-bit code for decoding mode

    // Internal signals for encoded and decoded outputs
    wire [6:0] encoded_code;
    wire [6:0] decoded_data;

    // Instantiating Hamming Controller
    hamming_controller hamming_inst (
        .data(data_in),
        .code(code_in),
        .mode(mode),
        .encoded_code(encoded_code),
        .decoded_data(decoded_data)
    );

    // Output assignments based on mode
    assign uo_out = (mode == 0) ? {1'b0, encoded_code} : {1'b0, decoded_data};

    assign uio_out = 8'b0;                 // Unused I/O output
    assign uio_oe  = 8'b0;                 // Unused I/O enable

    // Prevent warnings by listing unused inputs
    wire _unused = &{ena, clk, rst_n, uio_in, 1'b0};
endmodule

// Hamming Controller
module hamming_controller (
    input wire [3:0] data,           // 4-bit input data for encoding
    input wire [6:0] code,           // 7-bit input code for decoding
    input wire mode,                 // Mode selector: 0 for encode, 1 for decode
    output wire [6:0] encoded_code,  // Encoded output code
    output wire [6:0] decoded_data    // Decoded output data
);

    // Internal signals
    wire [6:0] encoder_code;         // Codeword output from encoder
    wire [6:0] decoder_data;         // Data output from decoder

    // Instantiating Hamming Encoder
    hamming_encoder encoder (
        .data(data),
        .code(encoder_code)
    );

    // Instantiating Hamming Decoder
    hamming_decoder decoder (
        .code(code),
        .data_out(decoder_data)
    );

    // // Output based on mode
    assign encoded_code = (mode == 0) ? encoder_code : 7'b0; // Output encoded code only in encoding mode
    assign decoded_data = (mode == 1) ? decoder_data : 7'b0; // Output decoded data only in decoding mode

endmodule