module top
    ( input clk
    , output led
    );

    reg rst = 1;
    always @(posedge clk) begin
        rst <= 0;
    end

    e_main main
        ( ._i_clk(clk)
        , ._i_rst(rst)
        , .__output(led)
        );
endmodule
