import sys
import os

print()

'''
python "this file" ".md to open and edit" "relative path to linkFile from assets" "linkFile extension"
'''

global numReplaced
numReplaced = 0

#returns absolute path to sysline filepath
def getFile():
    relativeFilename = sys.argv[1]

    # print("filename: ", relativeFilename)

    cwd = os.getcwd()

    # print("cwd: ", cwd)

    fullpath = cwd + "\\" + relativeFilename

    # print("Attempted path: ", fullpath)

    return fullpath


# returns line delimited by "#link "
def gethead(line):
    # print()
    # print("line: ", line)

    heads = line.split("#link ")

    # print("Heads: ", heads)

    # print()

    return heads

#takes in heads. If in form #(a-zA-Z0-9)* replaces eq head with [rest](.# "rest") where the non-hashtag = rest
def getReplacementStr(headers):
    # print("repl func:", len(headers)," ", headers)

    global numReplaced

    fillStr = headers[0]
    SlashN = False


    if (len(headers) == 2):
        if (len(headers[1].split("\n")) > 1): #pg# has \n
            headers[1] = headers[1].split("\n")[0]
            SlashN = True
    else: return fillStr
    
    # print()


    # print("Entry: ", entry)
    # print("Hashtags: ", hashtags)
    # print("len(entry delimit by #): ", len(hashtags))

    fillStr += "![page " + headers[1] + "]"

    fillStr += "(../assets/" + sys.argv[2] + headers[1] + sys.argv[3] + ")" + ("\n" if SlashN else "")  

    numReplaced += 1

    # print()

    # print("fillstr: ", fillStr)

    # print()
    
    return fillStr

def runFile(file):
    writeLinesLst = []
    while True:
        line = file.readline()

        #if eof, break loop
        if not line: break


        headLst = gethead(line)

        # print("Headlst:", len(headLst), " ", headLst)

        replacement = getReplacementStr(headLst)

        writeLinesLst.append(replacement)

    return writeLinesLst

filename = getFile()

f = open(filename, "r+")
WriteLines = runFile(f)
f.close()

# print("Writelines: ", WriteLines)

def replaceLines(filePath, linesToWrite):
    #print("lines after rewriting: ", lines[0])

    f = open(filePath, "w")

    f.writelines(linesToWrite)

    f.close()

replaceLines(filename, WriteLines)

#f = open(filename, "r")
#print("Lines from readfile: ", f.readlines())

print("num of #links replaced: ", numReplaced)
print()