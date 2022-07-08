#top = main::display_fsm
from spade import *

from cocotb.clock import Clock
from cocotb.triggers import FallingEdge

# Performs an SPI falling edge transition, and ensures that o is
# `new` in each subsequent clock
async def spi_state_transition(s: SpadeExt, clk, new):
    s.i.sclk_falling_edge = "true"
    await FallingEdge(clk)
    s.i.sclk_falling_edge = "false"
    s.o.assert_eq(new)
    await FallingEdge(clk)
    s.o.assert_eq(new)

@cocotb.test()
async def fsm(dut):
    s = SpadeExt(dut)

    clk = dut.clk_i

    await cocotb.start(Clock(clk, 1, units='ns').start())

    s.i.sclk_falling_edge = "false"
    s.i.t = "Timing$(us1: 5, us3: 15, mhz1: 5)"
    s.i.rst = "true"
    await FallingEdge(clk)
    s.i.rst = "false"

    for line in range(0, 3):
        print(f"{line}")
        # Initial state is CsLow
        s.o.assert_eq(f"State::CsLow({line}, 0)")

        # Wait low time (us1)
        [await FallingEdge(clk) for _ in range(0,5)]
        # Now high
        s.o.assert_eq(f"State::CsHigh({line}, 0)")

        # Wait low time (us1)
        [await FallingEdge(clk) for _ in range(0,5)]
        s.o.assert_eq(f"State::CsHigh({line}, 4)")

        await FallingEdge(clk)
        # Hold until spi falling edge
        s.o.assert_eq(f"State::CsHigh({line}, 4)")

        await spi_state_transition(s, clk, f"State::Mode({line})")
        await spi_state_transition(s, clk, f"State::FrameInv({line})")
        await spi_state_transition(s, clk, f"State::Clear({line})")
        for i in range(0, 5):
            await spi_state_transition(s, clk, f"State::FirstDummy({line}, {i})")

        # Address is sent correctly
        for i in range(0, 8):
            await spi_state_transition(s, clk, f"State::Address({line}, {i})")

        await spi_state_transition(s, clk, f"State::Data({line}, 0)")
        s.i.sclk_falling_edge = "true"
        for x in range(1, 400):
            # NOTE: We only check one line here in the interest of speed
            await FallingEdge(clk)
        s.i.sclk_falling_edge = "false"

        for x in range(0, 16):
            await spi_state_transition(s, clk, f"State::EndDummy({line}, {x})")

        s.i.sclk_falling_edge = "true"
        await FallingEdge(clk)
        s.i.sclk_falling_edge = "false"
        s.o.assert_eq(f"State::EndCsh({line}, 0)")
        [await FallingEdge(clk) for _ in range(0, 5)]

        # print(f"Done line {line} in {cocotb.utils.get_sim_time()}")

    # Wraparound
    # s.o.assert_eq(f"State::CsLow(0, 0)")


