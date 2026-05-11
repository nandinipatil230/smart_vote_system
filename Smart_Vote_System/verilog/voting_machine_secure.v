`timescale 1ns/1ps

module voting_machine_secure(

    input clk,
    input reset,

    input [3:0] voter_id,
    input [3:0] password,

    input vote_a,
    input vote_b,
    input vote_c,

    output reg [7:0] count_a,
    output reg [7:0] count_b,
    output reg [7:0] count_c,

    output reg invalid_password,
    output reg already_voted,
    output reg multiple_votes

);

reg voted [15:0];

parameter CORRECT_PASS = 4'b1010;

integer i;

always @(posedge clk or posedge reset)
begin

    if(reset)
    begin

        count_a <= 0;
        count_b <= 0;
        count_c <= 0;

        invalid_password <= 0;
        already_voted <= 0;
        multiple_votes <= 0;

        for(i=0; i<16; i=i+1)
        begin
            voted[i] <= 0;
        end

    end

    else
    begin

        invalid_password <= 0;
        already_voted <= 0;
        multiple_votes <= 0;

        // WRONG PASSWORD
        if(password != CORRECT_PASS)
        begin
            invalid_password <= 1;
        end

        // ALREADY VOTED
        else if(voted[voter_id] == 1)
        begin
            already_voted <= 1;
        end

        // MULTIPLE VOTES DETECTED
        else if((vote_a + vote_b + vote_c) > 1)
        begin
            multiple_votes <= 1;
        end

        // VALID VOTE
        else
        begin

            voted[voter_id] <= 1;

            if(vote_a)
            begin
                count_a <= count_a + 1;
            end

            else if(vote_b)
            begin
                count_b <= count_b + 1;
            end

            else if(vote_c)
            begin
                count_c <= count_c + 1;
            end

        end

    end

end

endmodule