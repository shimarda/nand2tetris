// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/4/Fill.asm

// Runs an infinite loop that listens to the keyboard input. 
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel. When no key is pressed, 
// the screen should be cleared.

//// Replace this comment with your code.
    // Put your code here:
        @R0
        M=0
        @R1
        M=0
(LOOP)  
        @KBD
        D=M
        @COLORBLACK
        D;JEQ
        @R0    //color
        M=0
        @PAINT
        0;JMP
(COLORBLACK)
        @R0    //color
        M=-1
        @PAINT
        0;JMP
(PAINT)
        @SCREEN
        D=A
        @8191
        D=D+A
        @R1  // Address 
        M=D
(FILL)
        @R0  // color
        D=M
        @R1
        A=M
        M=D
        @R1
        MD=M-1
        @SCREEN
        D=D-A
        @FILL
        D;JGE
        @LOOP
        0;JMP
(END)
        @END
        0;JMP
