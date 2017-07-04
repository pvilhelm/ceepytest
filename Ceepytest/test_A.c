#include <stdio.h>

/*#
print(r'printf("Hello from Ceepytest running test_A.c!"')
print(C0 + " A c-comment ")
print("Ceepytest captures stdout and writes it underneath the block" + C1)
#*/
 
/*# print("int") #*/ a = /*# print( 2+2, C+"So can this") #*/

void a_func(int a){
	//@reach	
	return;
}
 
int b_func(float b){
	return b+1.1;
}

//? b_func(1) == 2 
//? b_func(2) == 3
//? b_func(0) != 0

/*!
x = 1,2,3,4,5,6,7,8,9
ans = 2,3,4,5,6,7,8,10
!*/

/*?
b_func(@x) == @ans
?*/
