# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles

async def init_dut(dut):
    dut._log.info("Initializing DUT")

    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    # Reset
    dut._log.info("Resetting DUT")
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1


@cocotb.test()
async def validate_encoding(dut):
    await init_dut(dut)

    # Set the input values you want to test
    dut._log.info("Starting Hamming (7,4) Encoding Test Suite")
    dut._log.info("### Test Case 1: 4-Bit Inputs")
    test_cases_1 = {
        0b00000000: 0b00000000,
        0b00000001: 0b01101001,
        0b00000010: 0b00101010,
        0b00000011: 0b01000011,
        0b00000100: 0b01001100,
        0b00000101: 0b00100101,
        0b00000110: 0b01100110,
        0b00000111: 0b00001111,
        0b00001000: 0b01110000,
        0b00001001: 0b00011001,
        0b00001010: 0b01011010,
        0b00001011: 0b00110011,
        0b00001100: 0b00111100,
        0b00001101: 0b01010101,
        0b00001110: 0b00010110,
        0b00001111: 0b01111111
    }

    for data_input, expected_encoded in test_cases_1.items():
        dut.ui_in.value = data_input
        await ClockCycles(dut.clk, 1)

        if dut.uo_out.value == expected_encoded: 
            dut._log.info(f"PASS: Input {bin(data_input)[2:].zfill(4)} encoded correctly as {bin(expected_encoded)[2:].zfill(7)}")
        else:
            dut._log.error(
                f"FAIL: Input {bin(data_input)[2:].zfill(4)} encoding error. "
                f"Expected {bin(expected_encoded)[2:].zfill(7)}, got {bin(dut.uo_out.value)[2:].zfill(7)}"
            )
            assert dut.uo_out.value == expected_encoded, (
                f"Encoding failed for input {bin(data_input)[2:].zfill(4)}. "
                f"Expected {bin(expected_encoded)[2:].zfill(7)}, got {bin(dut.uo_out.value)[2:].zfill(7)}"
            )

    dut._log.info("### Test Case 2: 7-Bit Inputs")
    test_cases_2 = {
        0b00100000: 0b00000000,
        0b00100001: 0b01101001,
        0b00100010: 0b00101010,
        0b00100011: 0b01000011,
        0b00100100: 0b01001100,
        0b00100101: 0b00100101,
        0b00100110: 0b01100110,
        0b00100111: 0b00001111,
        0b00101000: 0b01110000,
        0b00101001: 0b00011001,
        0b00101010: 0b01011010,
        0b00101011: 0b00110011,
        0b00101100: 0b00111100,
        0b00101101: 0b01010101,
        0b00101110: 0b00010110,
        0b00101111: 0b01111111
    }

    for data_input, expected_encoded in test_cases_2.items():
        dut.ui_in.value = data_input
        await ClockCycles(dut.clk, 1)

        if dut.uo_out.value == expected_encoded: 
            dut._log.info(f"PASS: Input {bin(data_input)[2:].zfill(7)} encoded correctly as {bin(expected_encoded)[2:].zfill(7)}")
        else:
            dut._log.error(
                f"FAIL: Input {bin(data_input)[2:].zfill(4)} encoding error. "
                f"Expected {bin(expected_encoded)[2:].zfill(7)}, got {bin(dut.uo_out.value)[2:].zfill(7)}"
            )
            assert dut.uo_out.value == expected_encoded, (
                f"Encoding failed for input {bin(data_input)[2:].zfill(4)}. "
                f"Expected {bin(expected_encoded)[2:].zfill(7)}, got {bin(dut.uo_out.value)[2:].zfill(7)}"
            )

    dut._log.info("COMPLETED SUCCESSFULLY: Hamming Encoding Test Suite")

@cocotb.test()
async def validate_decoding(dut):
    await init_dut(dut)  # Initialize DUT at the start of the test

    # Define the encoded Hamming (7,4) codes
    codes = {
        0b00000000,
        0b01101001,
        0b00101010,
        0b01000011,
        0b01001100,
        0b00100101,
        0b01100110,
        0b00001111,
        0b01110000,
        0b00011001,
        0b01011010,
        0b00110011,
        0b00111100,
        0b01010101,
        0b00010110,
        0b01111111
    }

    dut._log.info("Starting Hamming (7,4) Decoding Test Suite")
    
    # Iterate through each encoded value and flip each bit
    for encoded in codes.items():
        for bit_position in range(7):
            # Flip the current bit
            flipped_code = encoded ^ (1 << bit_position)
            
            dut.ui_in.value = flipped_code
            await ClockCycles(dut.clk, 1)
            
            # Check if the decoded output matches the original encoded value
            if dut.uo_out.value == encoded: 
                dut._log.info(
                    f"PASS: Encoded {bin(encoded)[2:].zfill(7)}, "
                    f"flipped at position {bit_position}: {bin(flipped_code)[2:].zfill(7)}. " 
                    f"Decoded correctly to {bin(dut.uo_out.value)[2:].zfill(7)}"
                )
            else:
                dut._log.error(
                    f"FAIL: Encoded {bin(encoded)[2:].zfill(7)}, "
                    f"flipped at position {bit_position}: {bin(flipped_code)[2:].zfill(7)}"
                    f"Expected {bin(encoded)[2:].zfill(7)}, got {bin(dut.uo_out.value)[2:].zfill(7)}"
                )
                assert dut.uo_out.value == flipped_code, (
                    f"Decoding failed for encoded {bin(encoded)[2:].zfill(7)} "
                    f"with bit flipped at position {bit_position}: {bin(flipped_code)[2:].zfill(7)}"
                    f"Expected {bin(encoded)[2:].zfill(7)}, got {bin(dut.uo_out.value)[2:].zfill(7)}"
                )

    dut._log.info("COMPLETED SUCCESSFULLY: Hamming Decoding Test Suite")