#!/usr/bin/python
import sys, random, string, argparse

def shuf(linesInputted):
    random.shuffle(linesInputted) #shuffle the lines inputted     
    return linesInputted

def shufN(linesInputted,n): #shuffle when headcount specified
    inputList = []
    while n > 0:
        inputList.append(random.choice(linesInputted))
        n -= 1
    return inputList
        
def readFile(filename): #funtion that reads the file
    mylist =[]
    with open(filename,'r') as f: #opens the file for reading and associates the file with f
        for line in f:
            mylist.append(line.strip())
    return mylist

def main():

    parser = argparse.ArgumentParser() #creates an instance of Argument Parser

    parser.add_argument('-e','--echo',nargs= '+',help ='Treat each command-line operand as an input line')
    parser.add_argument('-i','--input-range', help = 'Treat each number LO through HI as an input line')
    parser.add_argument('-n','--head-count',help = 'Output as most COUNT lines')
    parser.add_argument('-r','--repeat', action = 'store_true',help = 'Output lines can be repeated')
    parser.add_argument ('input', nargs='?',help= 'Zero non-option argument, single non-option argument -,or file')

    args = parser.parse_args() #after parsing place input into args
    
    if args.echo:
        linesInputted = args.echo
    elif args.input_range:
        start, end = map(int,args.input_range.split('-')) #splits the string by the hyphen, in general map can help apply one fiction to everything in a list - here we are turning everything in out split into an integer and assign it to start, end respectively.
        linesInputted = list(range(start,end+1)) #get all the numbers between 0-9, but need to convert to a list because range is an iterable not a list

    #checking nonoptions                                                                                                                                                            
    else:
        if args.input == '-' or not args.input:
            linesInputted = sys.stdin.readlines()
            linesInputted = [line.rstrip() for line in linesInputted]
        elif args.input:
            linesInputted = readFile(args.input)

    if args.head_count:
        linesInputted = shufN(linesInputted,int(args.head_count))
            
    if args.repeat:
        if args.head_count and len(linesInputted) >= int(args.head_count):
            num = int(args.head_count)
            linesInputted = shufN(linesInputted,num)
        else:
            while True:
                print(random.choice(linesInputted))
        
    shuffledLines = shuf(linesInputted)

    for lines in shuffledLines:
       print(lines)
        
if __name__ == "__main__":
    main()
