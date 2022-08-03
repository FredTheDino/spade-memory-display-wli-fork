#top = main::display_output

from spade import *

from cocotb import triggers

@cocotb.test()
async def every_second_line_has_high_frame_inv(dut):
    s = SpadeExt(dut)

    s.i.state = "State::FrameInv(0)"
    await triggers.Timer(1, units='ps')
    s.o.assert_eq("Output::FrameInv(false)")

    s.i.state = "State::FrameInv(1)"
    await triggers.Timer(1, units='ps')
    s.o.assert_eq("Output::FrameInv(true)")

    s.i.state = "State::FrameInv(2)"
    await triggers.Timer(1, units='ps')
    s.o.assert_eq("Output::FrameInv(false)")


@cocotb.test()
async def line_index_is_output_lsb_first(dut):
    s = SpadeExt(dut)

    s.i.state = "State::Address(0b1100_1010, 0)"
    await triggers.Timer(1, units='ps')
    s.o.assert_eq("Output::Address(false)")

    s.i.state = "State::Address(0b1100_1010, 1)"
    await triggers.Timer(1, units='ps')
    s.o.assert_eq("Output::Address(true)")

    s.i.state = "State::Address(0b1100_1010, 2)"
    await triggers.Timer(1, units='ps')
    s.o.assert_eq("Output::Address(false)")

    s.i.state = "State::Address(0b1100_1010, 3)"
    await triggers.Timer(1, units='ps')
    s.o.assert_eq("Output::Address(true)")



