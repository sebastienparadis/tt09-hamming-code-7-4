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
    dut._log.info("Starting Hamming (7,4) Decoding Test Suite")
    dut._log.error("Decoding Test Suite Not Implemented, Skipping")
    pass