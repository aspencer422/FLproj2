
Description:
project 1 Description ( from Anthony Spencer submission )
Program works based off a DFA of 10 states. The program starts with an endless loop prompting user 
for float String input in the main method.  The main method also resets all global variables and 
call the start state of the DFA. The state methods all follow the same template of state actions 
first, then the checks for the next state.  If the state is a final state and the string is done 
the state call a function that builds the final number out of the three numbers possibly build 
from the DFA. If it is not a final state and the string ends, the string gets rejected. 
Also, if a char does not meet the output/input requirements for each state the string is rejected.  
The whole project was done with 10 states.  states q4,q5,q8,q9 are final states, 
while q1,q2,q6 and q7 are not final states.  Q3 was skipped as I found it redundant and decided
 to eliminate it completely.  

Project 2 Description:
Project 2 builds off of project 1.  All the final states from project one exits too appropriate project 2
states if possible.  We were able to accomplish the PDA to accept and calculate expressions.  States 1 - 10
are modified to be able to exit into project 2. states 10-15 were needed to solve project 2. The PDA uses
2 stacks to check the PDA, a operator stack and a parenthesis stack. The operator stack get pushed when an 
operator is read and popped when the second operand or a ending parenthesis ")".  The parenthesis stack gets 
pushed on '(' and popped on ')'. To handle spaces, we added another push/pop to the operator stack to keep 
track of the char before the space. this ensures we exit to the right state from a space. Out program  
creates the postfix stack as each char is read in.  The final state calls the solve postfix method to 
give our final answer.


State method template:
State(line,i):
# any action for given state
…..
 ….
# if/else checks for correct next state
If(I < line[i]-1)
	If (line[i+1] == ‘.’:
               …. 
                ….

#end