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

    o_mosi = s.o.mosi
    o_sclk = s.o.sclk
    o_cs = s.o.cs

    s.i.o = "proj::main::Output::UpdateMode()"
    await ensure_sclk_passthrough(s, o_sclk)
    await triggers.Timer(1, units='ps')
    

    # s.i.o = "proj::main::FrameInversion()"
    # s.i.o = "proj::main::AllClear()"
    # s.i.o = "proj::main::Dummy()"
    # s.i.o = "proj::main::Address()"
    # s.i.o = "proj::main::Pixel()"
    # s.i.o = "proj::main::CsHigh()"
    # s.i.o = "proj::main::CsLo()"
