#top = main::display_fsm
from spade import *

from cocotb.clock import Clock
from cocotb.triggers import FallingEdge

# Performs an SPI falling edge transition, and ensures that o is
# `new` in each subsequent clock
async def spi_state_transition(s: SpadeExt, clk, new):
    s.i.spi_falling_edge = "true"
    await FallingEdge(clk)
    s.i.spi_falling_edge = "false"
    # s.o().assert_eq(new)
    await FallingEdge(clk)
    # s.o().assert_eq(new)

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

    for line in range(0, 240):
        # Initial state is CsLow
        # s.o().assert_eq(f"proj::main::State::CsLow({line}, 0)")

        # Wait low time (us1)
        [await FallingEdge(clk) for _ in range(0,5)]
        # Now high
        # s.o().assert_eq(f"proj::main::State::CsHigh({line}, 0)")

        # Wait low time (us1)
        [await FallingEdge(clk) for _ in range(0,5)]
        # s.o().assert_eq(f"proj::main::State::CsHigh({line}, 4)")

        await FallingEdge(clk)
        # Hold until spi falling edge
        # s.o().assert_eq(f"proj::main::State::CsHigh({line}, 4)")

        await spi_state_transition(s, clk, f"proj::main::State::Mode({line})")
        await spi_state_transition(s, clk, f"proj::main::State::FrameInv({line})")
        await spi_state_transition(s, clk, f"proj::main::State::Clear({line})")
        for i in range(0, 5):
            await spi_state_transition(s, clk, f"proj::main::State::FirstDummy({line}, {i})")

        # Address is sent correctly
        for i in range(0, 8):
            await spi_state_transition(s, clk, f"proj::main::State::Address({line}, {i})")

        s.i.spi_falling_edge = "true"
        for x in range(0, 400):
            # await spi_state_transition(s, clk, f"proj::main::State::Data({line}, {x})")
            await FallingEdge(clk)

        for x in range(0, 16):
            await spi_state_transition(s, clk, f"proj::main::State::EndDummy({line}, {x})")

        s.i.spi_falling_edge = "true"
        await FallingEdge(clk)
        s.i.spi_falling_edge = "false"
        # s.o().assert_eq(f"proj::main::State::EndCsh({line}, 0)")
        [await FallingEdge(clk) for _ in range(0, 5)]

        print(f"Done line {line} in {cocotb.utils.get_sim_time()}")

    # Wraparound
    s.o().assert_eq(f"proj::main::State::CsLow(0, 0)")


