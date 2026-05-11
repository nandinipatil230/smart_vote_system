`timescale 1ns/1ps

module voting_machine_secure_tb;

reg clk;
reg reset;
reg [3:0] voter_id;
reg [3:0] password;
reg vote_a;
reg vote_b;
reg vote_c;

wire [7:0] count_a;
wire [7:0] count_b;
wire [7:0] count_c;

wire invalid_password;
wire already_voted;
wire multiple_votes;

voting_machine_secure uut(
    .clk(clk),
    .reset(reset),
    .voter_id(voter_id),
    .password(password),
    .vote_a(vote_a),
    .vote_b(vote_b),
    .vote_c(vote_c),
    .count_a(count_a),
    .count_b(count_b),
    .count_c(count_c),
    .invalid_password(invalid_password),
    .already_voted(already_voted),
    .multiple_votes(multiple_votes)
);

always #5 clk = ~clk;

initial
begin

    clk = 0;
    reset = 1;

    #10;
    reset = 0;

    $display("Time\tID\tA\tB\tC\tInvalid\tAlready\tMultiple");

    $monitor("%0t\t%d\t%d\t%d\t%d\t%d\t%d\t%d",
        $time,
        voter_id,
        count_a,
        count_b,
        count_c,
        invalid_password,
        already_voted,
        multiple_votes
    );

    voter_id = 1;
    password = 4'b1010;
    vote_a = 1;
    vote_b = 0;
    vote_c = 0;

    #10;

    voter_id = 2;
    password = 4'b1010;
    vote_a = 0;
    vote_b = 1;
    vote_c = 0;

    #10;

    voter_id = 1;
    password = 4'b1010;
    vote_a = 1;
    vote_b = 0;
    vote_c = 0;

    #10;

    voter_id = 3;
    password = 4'b1111;
    vote_a = 1;
    vote_b = 0;
    vote_c = 0;

    #50;

    $finish;

end

endmodule