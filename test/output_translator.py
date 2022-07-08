#top = main::output_translator

from spade import *

from cocotb.clock import Clock

async def ensure_sclk_passthrough(s, o):
    s.i.sclk = "true"
    await triggers.Timer(1, units='ps')
    o.assert_eq("true")
    s.i.sclk = "false"
    await triggers.Timer(1, units='ps')
    o.assert_eq("false")

@cocotb.test()
async def fsm(dut):
    s = SpadeExt(dut)

    o_sclk = s.o.sclk

    s.i.o = "Output::UpdateMode()"
    await ensure_sclk_passthrough(s, o_sclk)
    s.o.mosi.assert_eq("true")

    s.i.o = "Output::FrameInv(true)"
    await ensure_sclk_passthrough(s, o_sclk)
    s.o.mosi.assert_eq("true")
    s.i.o = "Output::FrameInv(false)"
    await ensure_sclk_passthrough(s, o_sclk)
    s.o.mosi.assert_eq("false")

    s.i.o = "Output::AllClear()"
    await ensure_sclk_passthrough(s, o_sclk)
    s.o.mosi.assert_eq("false")

    s.i.o = "Output::Dummy()"
    await ensure_sclk_passthrough(s, o_sclk)
    s.o.mosi.assert_eq("false")

    s.i.o = "Output::Address(false)"
    await ensure_sclk_passthrough(s, o_sclk)
    s.o.mosi.assert_eq("false")
    s.i.o = "Output::Address(true)"
    await ensure_sclk_passthrough(s, o_sclk)
    s.o.mosi.assert_eq("true")

    s.i.o = "Output::Pixel(true)"
    s.o.mosi.assert_eq("true")
    s.i.o = "Output::Pixel(false)"
    await ensure_sclk_passthrough(s, o_sclk)
    s.o.mosi.assert_eq("false")

    s.i.sclk = "true"
    s.i.o = "Output::CsHigh()"
    await triggers.Timer(1, units='ps')
    s.o.mosi.assert_eq("false")
    s.o.sclk.assert_eq("false")
    s.o.cs.assert_eq("true")

    s.i.o = "Output::CsLow()"
    await triggers.Timer(1, units='ps')
    s.o.mosi.assert_eq("false")
    s.o.sclk.assert_eq("false")
    s.o.cs.assert_eq("false")
    # s.i.o = "Output::CsLow()"
