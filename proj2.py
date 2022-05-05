#-------------------------------------------------------------------------
# AUTHOR: Anthony Spencer, Alex Hernandez
# FILENAME: proj2.py
# SPECIFICATION: reads in string and run DFA to biuld float 
#                calculate expressions 
#                
# FOR: CS 3110 Formal Lang
#-----------------------------------------------------------------------*/


#GLOBALS VARS
#from ast import operator


front=0
decimal=0
decCount=1
exp=0
expFlag = False 
expSign=1
l=['0','1', '2','3' '4', '5', '6', '7', '8', '9', '+', '-', '.', '_', 'e', 'E', 'f', 'F', 'd', 'D']
digits = ['0','1', '2','3', '4', '5', '6', '7', '8', '9']
signs=['+', '-']
e=['e', 'E']
fnd=['f', 'F', 'd', 'D']
priority = {'+':1, '-':1, '*':2, '/':2}
operators = set(['+', '-', '*', '/']) 

#PDA stacks
pdaOpStack = []
pdaParStack = []

#calulation stacks (not part of PDA)
postFixStack = []
converterStack = []



###########################################################################
#   main()
#   driver methods that takes in pinput and starts DFA on endless loop
#   Input: void
#   returns: void
###########################################################################

def main():

    entry =' '
    
    while(entry != 'q' or entry != 'Q'):
        #call all globals
        global front 
        global decimal
        global decCount
        global exp
        global expFlag 
        global expSign
        global pdaOpStack
        global pdaParStack
        global postFixStack
        global converterStack

        #reset all globals
        front=0
        decimal=0
        decCount=1
        exp=0
        expFlag = False
        expSign=1
        pdaOpStack= []
        pdaParStack= []
        postFixStack= []
        converterStack= []

        print("Enter Java Float String (enter q to quit):")
        entry =' '
        entry = input(">>> ")

        if (entry == 'q' or entry == 'Q'):
            break
        else:
            if(len(entry) > 0):
                startState(entry)
            else:
                print("please input string with at least one char")

###########################################################################
#   startState(string)
#   start state of DFA
#   Input: String, index
#   returns: void
###########################################################################
def startState(line):
    #actions 
    i=0
    char = line[i]

    #checks and calls for next state
    if (char in digits):
        #print('call state 1')
        q1(line,i)
    elif(char =='.'):
        #print('call state 2')
        q2(line,i)
    elif(char =='('):
        q11(line,i)
    else:
        print('rejected at Start state')

###########################################################################
#   q1(line,i)
#   state 1:  triggered on digits from q0,q1,q10
#   Input: digits
#   returns: Void
#   exit on .:q4 , F:q9 , _:q10
###########################################################################

def q1(line,i):
    global front
    #actions
    if line[i] != '_':
        char = line[i]

        num = ord(char)-ord('0')

        front = front * 10
        front = front + num
    #next state calls
    if( i < (len(line)-1)):
        if(line[i+1] in digits):
            q1(line,i+1)
        elif(line[i+1] == '.'):
            #print('call q4')
            q4(line,i+1)
        elif(line[i+1] in fnd):
            #print('call q9') 
            q9(line,i+1)
        elif(line[i+1] == '_'):
            #remember underscore need a return to value
            #print('call q10')
            q1(line,i+1)
        elif(line[i+1] in e):
            q6(line,i+1)
        else:
            print('Rejected: not valid output of q1 (not a final state)')
    else:
        print('rejected: ended on q1 (not a final state)')
        #print(front)


###########################################################################
#   q2(line,i)
#   state 2:  triggered on . from q0
#   Input: .
#   returns: Void
#   exit digits:q5
###########################################################################

def q2(line,i):
    #action = none 

    #next state calls
    if( i < (len(line)-1)):
        if(line[i+1] in digits):
            q5(line,i+1)
        else:
            print('Rejected: invalid entry to q2 ')
    else:
        print('Rejected: ended on q2 (not a final State')

#note q3 ended up not being needed 

###########################################################################
#   q4(line,i)
#   FINAL STATE
#   state 4:  triggered on . from q1
#   Input: .
#   returns: Void
#   exit digits:q5 , F:q9
###########################################################################

def q4(line,i):
    #action = none 

    #next state calls
    if( i < (len(line)-1)):
        if(line[i+1] in digits):
            q5(line,i+1)
        elif(line[i+1] in fnd):
            #print('call q9')
            q9(line,i+1)
        elif(line[i+1] == ')'):
            buildFloat()
            q12(line,i+1)
            #print("biuld andpass to ) state")
        elif(line[i+1] in operators):
            buildFloat()
            q13(line,i+1)
            #
            pass
        elif(line[i+1] == ' '):
            buildFloat()
            pdaOpStack.append('#')
            q14(line,i+1)
            #print("biuld andpass to space state")
        else:
            print('Rejected: not valid output of q4 ')
    else:
        buildFloat()
        q15(line,i)
        #add calc postfix 

###########################################################################
#   q5(line,i)
#   FINAL STATE
#   state 5:  triggered on digits From q4
#   Input: digits:q4,q5,q2
#   returns:  Void
#   exits digits:q5 , F:q9 , E:q6
###########################################################################
def q5(line,i):
    global decCount
    global decimal
    #Actions
    char = line[i]
    num = ord(char) - ord('0')

    num = num / (10**decCount)
    decCount = decCount +1
    decimal = decimal+num

    #next state calls
    if( i < (len(line)-1)):
        if(line[i+1] in digits):
            q5(line,i+1)
        elif(line[i+1] in fnd):
            #print('call q9')
            q9(line,i+1)
        elif(line[i+1] in e):
            q6(line,i+1)
        elif(line[i+1]=='_'):
            #print('call q10')
            q10(line,i+1,5)
        elif(line[i+1] == ')'):
            buildFloat()
            q12(line,i+1)
            #print("biuld andpass to ) state")
        elif(line[i+1] in operators):
            buildFloat()
            q13(line,i+1)
            #print("biuld and pass to operator state")
            pass
        elif(line[i+1] == ' '):
            buildFloat()
            pdaOpStack.append('#')
            q14(line,i+1)
            #print("biuld andpass to space state")
        else:
            print('Rejected: not valid output of q5 ')
    else:
        
        buildFloat()
        q15(line,i)
        #add calc postfix

###########################################################################
#   q6(line,i)
#   state 6:  triggered on E From q5,q1
#   Input: E:q5,q1
#   returns:  Void
#   exits digits:q8 , F:q9 , signs:q7
###########################################################################

def q6(line,i):
    #action = none 

    #next state calls
    if( i < (len(line)-1)):
        if(line[i+1] in signs):
            q7(line,i+1)
        elif(line[i+1] in digits):
            q8(line,i+1)
        else:
            print('Rejected: not valid output of q6 (not a final state)')
    else:
        print('Rejected: ended on q6 (not a final state)')

###########################################################################
#   q7(line,i)
#   state 7:  triggered on signs From q6
#   Input: signs:q6
#   returns:  Void
#   exits digits:q8
###########################################################################

def q7(line,i):
    global expSign
    #action  
    if(line[i]=='-'):
        expSign = -1

    #next state calls
    if( i < (len(line)-1)):
        if(line[i+1] in digits):
            q8(line,i+1)
        else:
            print('Rejected: not valid output of q7 (not a final state)')
    else:
        print('Rejected: ended on q7 (not a final state)')

###########################################################################
#   q8(line,i)
#   FINAL STATE
#   state 8:  triggered on Digits From q6,q7,q8 
#             biulds exponent value
#   Input: digits :q6,q7,q8
#   returns:  Void
#   exits DnF:q9, digits :q8
###########################################################################

def q8(line,i):
    global exp
    global expFlag
    #action  
    expFlag = True
    char = line[i]

    num = ord(char)-ord('0')

    exp = exp * 10
    exp = exp + num

    #next state calls
    if( i < (len(line)-1)):
        if(line[i+1] in digits):
            q8(line,i+1)
        elif(line[i+1] in fnd):
            q9(line,i+1)
        elif(line[i+1] == '_'):
            #remember underscore need a return to value
            #print('call q10')
            q10(line,i+1,8)
        elif(line[i+1] == ')'):
            buildFloat()
            q12(line,i+1)
            #print("biuld andpass to ) state")
        elif(line[i+1] in operators):
            buildFloat()
            q13(line,i+1)
            #
            pass
        elif(line[i+1] == ' '):
            buildFloat()
            pdaOpStack.append('#')
            q14(line,i+1)
            #print("biuld andpass to space state")
        else:
            print('Rejected: not valid output of q8)')
    else:
        buildFloat()
        q15(line,i)
        #add calc postfix 

###########################################################################
#   q9(line,i)
#   FINAL STATE
#   state 8:  triggered on F/D From q1,q4,q5,q8 call float biulder 
#   Input: F/D :q1,q4,q5,q8
#   returns:  Void
#   exits no EXIT 
###########################################################################

def q9(line,i):
    
    #action = none 

    #next state calls
    if (  i < (len(line)-1)):
        #add calc postfix
        if(line[i+1] == ')'):
            buildFloat()
            q12(line,i+1)
            #print("biuld andpass to ) state")
        elif(line[i+1] in operators):
            buildFloat()
            q13(line,i+1)
            #
            pass
        elif(line[i+1] == ' '):
            buildFloat()
            pdaOpStack.append('#')
            q14(line,i+1)
            #print("biuld andpass to space state")
    else:
        buildFloat()
        q15(line,i)
        

###########################################################################
#   q10(line,i,back)
#   state 8:  triggered on _ From q1,q5,q8
#             Back var keeps track of what was called
#             kept this in because adding Space to the digit states(q1,q5,q8) 
#             would allow for 34_.  or 3.42_ 
#             could be 3 differnt states but added back var for less repeat code. 
#   Input: _:q1,q5,q8  
#   returns:  Void
#   exits digits:q1,q5,q8
###########################################################################

def q10(line,i,back):
    #action = none 

    #next state calls
    if( i < (len(line)-1)):
        if(line[i+1] in digits):
            if(back ==1):
                q1(line,i+1)
            elif(back ==5):
                q5(line,i+1)
            elif(back == 8):
                q8(line,i+1)
        elif(line[i+1] == '_'):
            #remember underscore need a return to value
            q10(line,i+1,back)
        else:
            print('Rejected: not valid output of q10 (not a final state)')
    else:
        print('Rejected: ended on q10 (not a final state)' + str(front))

###########################################################################
#   q11(line,i,back)
#   state 11:  (
#   Input: _:q1,q5,q8  
#   returns:  Void
#   exits digits:q1,q5,q8
###########################################################################

def q11(line,i):
    #action = none 
    pdaParStack.append('(')
    converterStack.append('(')
    #next state calls
    if( i < (len(line)-1)):
        if(line[i+1] in digits):
            q1(line,i+1)
        elif(line[i+1] == '.'):
            q2(line,i+1)
        elif(line[i+1] == '('):
            q11(line,i+1)
        elif(line[i+1] == ' '):
            pdaOpStack.append(line[i])
            q14(line,i+1)
    else:
        print('Rejected: ended on q11 (not a final state)' )

###########################################################################
#   q12(line,i,back)
#   state 12:  )
#   Input: _:q1,q5,q8  
#   returns:  Void
#   exits digits:q1,q5,q8
###########################################################################

def q12(line,i):
    #action = none 
    pdaParStack.pop()
    #pdaOpStack.pop()
    while converterStack and converterStack[-1]!= '(':
        postFixStack.append(converterStack.pop())
    converterStack.pop()
    #next state calls
    if( i < (len(line)-1)):
        if(line[i+1] in operators):
            q13(line,i+1)
        elif(line[i+1] == ')'):
            q12(line,i+1)
        elif(line[i+1] == ' '):
            pdaOpStack.append(line[i])
            q14(line,i+1)
        else:
            print('Rejected: ended on q12 (not a final state)')
    elif(i == (len(line)-1)):
        q15(line, i)
    else:
        print('Rejected: ended on q12 (not a final state)')

###########################################################################
#   q13(line,i,back)
#   state 13:  operators
#   Input: _:q1,q5,q8  
#   returns:  Void
#   exits digits:q1,q5,q8
###########################################################################

def q13(line,i):
    #action = none 
    pdaOpStack.append(line[i])
    while converterStack and converterStack[-1]!='(' and priority[line[i]]<=priority[converterStack[-1]]:
        postFixStack.append(converterStack[-1])
        converterStack.pop()

    converterStack.append(line[i])
    #next state calls
    if( i < (len(line)-1)):
        if(line[i+1] in digits):
            pdaOpStack.pop()
            q1(line,i+1)
        elif(line[i+1] == '.'):
            pdaOpStack.pop()
            q2(line,i+1)
        elif(line[i+1] == '('):
            pdaOpStack.pop()
            q11(line,i+1)
        elif(line[i+1] == ' '):
            pdaOpStack.append(line[i])
            q14(line,i+1)
    else:
        print('Rejected: ended on q13 (not a final state)' + str(front))

###########################################################################
#   q14(line,i,back)
#   state 14: SPACE
#   Input: _:q1,q5,q8  
#   returns:  Void
#   exits digits:q1,q5,q8
###########################################################################

def q14(line,i):
    #action = none 

    #next state calls
    if( i < (len(line)-1)):
        if(pdaOpStack[-1]=='#'):
            if(line[i+1] in operators):
                pdaOpStack.pop()
                q13(line,i+1)
            elif (line[i+1] == ')'):
                pdaOpStack.pop()
                q12(line,i+1)
            else:
                print('Rejected:    space from # to invalid: ' + str(line[i+1]))
        elif(pdaOpStack[-1]=='(' or pdaOpStack[-1]in operators):
            if(line[i+1] in digits):
                pdaOpStack.pop()
                if pdaOpStack[-1]in operators:
                    pdaOpStack.pop()
                q1(line,i+1)
            elif(line[i+1] =='.'):
                pdaOpStack.pop()
                if pdaOpStack[-1]in operators:
                    pdaOpStack.pop()
                q2(line,i+1)
            elif (line[i+1] == '('):
                if pdaOpStack[-1]in operators:
                    pdaOpStack.pop()
                pdaOpStack.pop()
                q11(line,i+1)
            else:
                print('Rejected:    space from ( or ops to invalid: ' + str(line[i+1]))
        elif(pdaOpStack[-1]==')'):
            if(line[i+1] in operators):
                pdaOpStack.pop()
                q13(line,i+1)
            elif (line[i+1] == ')'):
                pdaOpStack.pop()
                q12(line,i+1)
            else:
                print('Rejected:    space from ) to invalid: ' + str(line[i+1]))
    else:
        print('Rejected: ended on q14 (not a final state)' )

###########################################################################
#   q15(line,i,back)
#   state 15:  end state
#   Input: _:q1,q5,q8  
#   returns:  Void
#   exits digits:q1,q5,q8
###########################################################################

def q15(line,i):
    #action = none 
    

    while converterStack:

        postFixStack.append(converterStack.pop())
    #next state calls
    print('Final postFix: ' + str(postFixStack))
    print('PDA par stack : ' + str(pdaParStack))
    print('PDA ops stack : ' + str(pdaOpStack))
    
    calculateStack = []
    for i in postFixStack:
        if (i in operators):
            if(i == '+'):
                calculateStack.append(calculateStack.pop() + calculateStack.pop())
            elif(i == '-'):
                x = calculateStack.pop()
                y = calculateStack.pop()
                z = y - x
                calculateStack.append(z)
            elif(i == '*'):
                calculateStack.append(calculateStack.pop() * calculateStack.pop())
            else:
                x = calculateStack.pop()
                y = calculateStack.pop()
                z = y / x
                calculateStack.append(z)
        else:
            calculateStack.append(i)

    print("Final Result = "+ str(calculateStack[-1]))

        
###########################################################################
#   printFinal()
#   constructs final float from glabal vars
#   Input: VIOD
#   returns:  Void
###########################################################################

def buildFloat():
    global front 
    global decimal
    global decCount
    global exp
    global expFlag 
    global expSign

    result = 0.0


    if(decimal != 0):
        result = front + decimal
    else:
        result = front + 0.0
    
    if(expFlag == True):
        result = result * ((10**exp)**expSign)

    postFixStack.append(result)
            #call all globals


    #reset all globals
    front=0
    decimal=0
    decCount=1
    exp=0
    expFlag = False
    expSign=1



# call main
if __name__=="__main__":
    main()