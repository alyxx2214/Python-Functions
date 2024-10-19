import sys
import os

global numReplaced
numReplaced = 0

print()

'''
python "this file" ".md to open and edit" "relative path to linkFile from assets" "linkFile extension"
'''

#returns absolute path to sys.arg[1] filepath (the .md file in {graph}/pages/)
def getFile():
    relativeFilename = sys.argv[1]

    # print("filename: ", relativeFilename)

    cwd = os.getcwd()

    # print("cwd: ", cwd)

    fullpath = cwd + "\\" + relativeFilename

    # print("Attempted path: ", fullpath)

    return fullpath


# returns list of line delimited by "#xlink "
def gethead(line):
    heads = line.split("#xlink ")

    return heads

#takes in heads. If in form #(a-zA-Z0-9)* replaces eq head with [rest](.# "rest") where the non-hashtag = rest
def getReplacementStr(headers):
    #import global num of changed #xlinks
    global numReplaced

    #fill starts as all the stuff before the #xlink
    fillStr = headers[0]
    
    #if headers 1 elem, there is no #xlink in the head; return unchanged head
    if(len(headers) < 2): return fillStr
    

    '''
    argmt = #xlink "part of file that changes" "file location from ../assets/":"file extension"|
    
    for example:
    
    i'm taking notes oh heres the slides: 
    #xlink _00_Introduction:Class/Slides/NAME Slide_conveNtion:.pdf|
    # you can continue notes lah dee dah    
    '''
    #btw "#xlink " and "|" 
    argmts = headers[1].split("|")[0]
    
    if (len(argmts.split(":")) < 3):
        print(f"<< WARNING: ARGMS MISSING ({len(argmts)} < 3) | argmts = {argmts}")
    elif (len(argmts.split(":")) > 3):
        print(f"<< WARNING: EXTRA ARGMS ({len(argmts)} > 3) | argmts = {argmts}")

    #entry 1
    fileNameDescr = argmts.split(":")[0]
    #entry 2
    left = argmts.split(":")[1]
    #entry 3
    right = argmts.split(":")[2]

    #annotating to user
    print(f" >> replacing \"#xlink {argmts}|\" with \"![link: {fileNameDescr}](../assets/{left}{fileNameDescr}{right})\"") #debug

    #essentially replacing {#xlink argmt} with {![link $fileNameDescr](../assets/$left$fileNameDescr$right) }
    fillStr += f"![link: {fileNameDescr}](../assets/{left}{fileNameDescr}{right})"

    numReplaced += 1

    #if there is stuff after the "|" but befor the next theoretical "#xlink ", add that stuff to fillStr
    #if there is no stuff after the "|", the error will be caught and fillstr ends here (plus the next "#xlink ")
    try:
        fillStr += headers[1].split("|")[1]
    except:
        #print("Nothing after \"|\": ", headers[1])
        fillStr += ""
    
    #if there are more than 1 "#xlink " in the line, then len(headers) > 2
    #when this happens, we make the new array {"", headers[2], headers[3], ..., headers[len(headers)-1]}
    #this will return a new string where "" comes b4 the "#xlink", and any additional "#xlink " will be taken care of by recursion :)
    if (len(headers) > 2):
        #saying that next working line starts w "#xlink "
        newHeaders = [""]

        #for each head in headers (except 1st 2 entries), add head to new headers
        for i in headers[2:]:
            newHeaders.append(i)

        #the string we'll tack onto our line is this same current function, but with the new headers
        nextXlink = getReplacementStr(newHeaders)
        
        #add that function return to fillStr
        fillStr += " " + nextXlink
        
    
    #return the line, now that all its "#xlink " refs have been taken care of
    return fillStr

#runs the list of lines from file
def runFile(file):
    #set of lines file is replaced with
    writeLinesLst = []

    #for each line in file
    while True:
        #save current line
        line = file.readline()

        #if eof, break loop
        if not line: break

        #get line delimited by #xlink
        headLst = gethead(line)

        #get replacement string
        replacement = getReplacementStr(headLst)

        #add string to list to write back to file
        writeLinesLst.append(replacement)

    return writeLinesLst

#get filename
filename = getFile()


#open the file with read
f = open(filename, "r")
WriteLines = runFile(f)
f.close() #close reading file

#writes a list of lines to the file
def replaceLines(filePath, linesToWrite):
    f = open(filePath, "w")

    f.writelines(linesToWrite)

    f.close()

#replace the file contents with its rewritten lines
replaceLines(filename, WriteLines)

#f = open(filename, "r")
#print("Lines from readfile: ", f.readlines())

print("\nnum #xlinks replaced: ", numReplaced, "\n")
print()