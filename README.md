# Ceepy Test
### A pytonic PHP/JSP wanna-be C testing framework

Ceepy is a tool to write unit tests for C projects. By writing inline Ceepy formatted code in a 
.c-file Ceepy generates a test with fancy asserts and outputs in C code.

## For whom is Ceepy?

For anyone that thinks it's tedious writing verbose tests with pure C frameworks and don’t want to use impure C++ frameworks (like [Catch]( https://github.com/philsquared/Catch)) to tests their C code. 

## Requirements
-	Python 3.6 (Other 3+ might work)
-	A C compiler

## Code example

```
/* silly_example.ct */

int add(int a, int b){ /* Your functions to test should be in separate .c-file normaly */
  return a+b;
}

//! int add() § Redeclare return type of the function for Ceepy

/*?   					  § This is an assert block
add(1,1) < 3 			§ If one of these asserts fail the test fails
add(10,10) == 10 + 10
add(20,30) != 0
?*/

/* 
 * All functions that begin with "test_" and returns an int are added 
 * to the generated test and called during test. In these functions
 * we can add c-code and do Ceepy style assert with local variables. 
 */
 
void init_thing(){/* Bla bla */}
float do_interesting_thing(){return 10101;}

int test_silly(){ 
  init_thing();
  float ans = do_interesting_thing();
  //% ans >= # sin(2.3)*0.5   §With "#" you can call Python code inline
  return 0; /* Return 0 on success */
}
```
Then execute ceepy in the same directory as the example file is in or specify absolute paths to generate the .c files for the test. 

On Windows from VS developer prompt:
```
py ceepy -f silly_example.ct -t silly_example
cd silly_example
compile.bat
silly_example.exe
```
On a Posix:
Use gcc. You know what to do ;)

## Manual

Coming soon(tm).  
