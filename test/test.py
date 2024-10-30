# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles


@cocotb.test()
async def test_project(dut):
    dut._log.info("Start")

    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    # Reset
    dut._log.info("Reset")
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1

    dut._log.info("Test project behavior")

    # Set the input values you want to test

    # Test Encoding (mode = 0, 4-bit data = 1010)
    dut._log.info("Testing Encoding Mode with Data Input: 1010")
    dut.ui_in.value = 0b00001010  # 4-bit data with MSB (ui_in[7]) = 0 for encoding mode
    await ClockCycles(dut.clk, 1)
    # Check expected encoded output
    # Expected encoded result: parity + data = 1011010
    expected_encoded = 0b1011010
    assert dut.uo_out.value == expected_encoded, f"Encoding failed, got {dut.uo_out.value}, expected {expected_encoded}"

    # Test Decoding (mode = 0, 4-bit code = 00001111)
    dut._log.info("Testing Encoding Mode with Data Input: 1111")
    dut.ui_in.value = 0b00001111  # 7-bit code with MSB (ui_in[7]) = 1 for decoding mode
    await ClockCycles(dut.clk, 1)

    # Expected corrected code: 1101010, decoded data: 1010
    expected_encoded = 0b1111111
    assert dut.uo_out.value == expected_encoded, f"Encoding failed, got {dut.uo_out.value}, expected {expected_encoded}"

    dut._log.info("Hamming Code Test completed successfully")

    # Change it to match the actual expected output of your module:

    # Keep testing the module by changing the input values, waiting for
    # one or more clock cycles, and asserting the expected output values.


@cocotb.test()
async def validate_encoding(dut):
    dut._log.info("Starting Hamming (7,4) Encoding Test Suite")
    test_cases = {
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

    for data_input, expected_encoded in test_cases.items():
        dut.ui_in.value = data_input
        await ClockCycles(dut.clk, 1)

        if dut.uo_out.value == expected_encoded: 
            f"PASS: Input {bin(data_input)[2:].zfill(4)} encoded correctly as {bin(expected_encoded)[2:].zfill(7)}" 
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
    pass