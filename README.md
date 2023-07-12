# THIS IS A FORK
This version is not actively maintained. Unless you came from a thesis the changes presented here are not of interest to you, and you probably meant to go to https://gitlab.com/TheZoq2/spade-memory-display/-/tree/main

# Memory Display

Spade driver for the adafruit sharp memory display
https://www.adafruit.com/product/4694.

## Usage instructions


```spade
use memory_display::main::OutputPins;
use memory_display::main::Output;
use memory_display::main::Timing;
use memory_display::main::display_gen;
use memory_display::main::output_translator;

entity top(clk: clk, rst: bool) -> OutputPins {
    // Create a timing struct and provide the durations of the fields at your target
    // frequency
    let t = Timing$(
        us1: 12,
        us3: 36,
        mhz1: 6
    );

    // Instantiate the `display_gen` entity
    let display_signals = inst display_gen(clk, rst, t);

    let offset = 0;

    // Translate the pixel coordinates of the output into boolean pixel values. This
    // example generates a checkerboard pattern with an offset

    let with_pixels = match display_signals.o {
        Output::UpdateMode => Output::UpdateMode(),
        Output::FrameInv(v) => Output::FrameInv(v),
        Output::AllClear => Output::AllClear(),
        Output::Dummy => Output::Dummy(),
        Output::Address(v) => Output::Address(v),
        Output::Pixel((x, y)) => {
            Output::Pixel((x + offset & 0b10000) == (sext(y) + offset & 0b10000))
        },
        Output::CsHigh => Output::CsHigh(),
        Output::CsLow => Output::CsLow(),
    };

    // Generate the spi clk, mosi and chip select signals by calling the output translator
    function
    output_translator(with_pixels, display_signals.sclk)
}
```
