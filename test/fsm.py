#top = main::display_fsm
from spade import *

from cocotb.clock import Clock
from cocotb.triggers import FallingEdge

@cocotb.test()
async def fsm(dut):
    s = SpadeExt(dut)

    clk = dut.clk_i

    await cocotb.start(Clock(clk, 1, units='ns').start())

    s.i.spi_falling_edge = "false"
    s.i.t = "proj::main::Timing$(us1: 5, us3: 15)"
    s.i.rst = "true"
    await FallingEdge(clk)
    s.i.rst = "false"

    # Initial state is CsLow
    s.o().assert_eq("proj::main::State::CsLow(0, 0)")

    # Wait low time (us1)
    [await FallingEdge(clk) for _ in range(0,5)]
    # Now high
    s.o().assert_eq("proj::main::State::CsHigh(0, 0)")

    # Wait low time (us1)
    [await FallingEdge(clk) for _ in range(0,5)]
    s.o().assert_eq("proj::main::State::CsHigh(0, 4)")

    await FallingEdge(clk)
    # Hold until spi falling edge
    s.o().assert_eq("proj::main::State::CsHigh(0, 4)")

    s.i.spi_falling_edge = "true"
    await FallingEdge(clk)
    s.o().assert_eq("proj::main::State::Mode(0)")

