module top
    ( input clk
    , output sclk
    , output mosi
    , output cs
    );

    reg rst = 1;
    always @(posedge clk) begin
        rst <= 0;
    end

    e_proj_hw_test__top main
        ( .clk_i(clk)
        , .rst_i(rst)
        , .output__({sclk, cs, mosi})
        );
endmodule
