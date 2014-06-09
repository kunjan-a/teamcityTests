#!/usr/bin/python
import sys
import getopt
import os
import json
import types
import datetime


#Print help for the cmdline usage
def printusage():
    print 'Usage:'
    print 'configSetter.py -e <sourceEnvironment> -c <configPath> -d <dateConfigKey> -o <outputFileName>'
    print 'The paths should be relative to the current working directory.'
    print 'The sourceEnvironment is used to search for a properties file `env.<sourceEnvironment>.properties`' \
          ' inside the given <configPath>'
    print 'The properties file is copied as `<outputFileName>.properties` file inside <configPath>.'
    print 'An extra data key is added in the properties file created above with key `<dateConfigKey>` and value `ddmmmyyyy`.'

    print '\n*******************************************\ne.g. for go.to run this command from gandalf:\n' \
      '  ./scripts/configSetter.py -e market -c app/assets/config -d app.build_date -o goto'


#Fetch the cmdline args and exit in case of improper usage
def getargs(argv):
    if len(argv) < 8:
        printusage()
        sys.exit(2)
    inputfile = ''
    configPath = ''
    outputfile = ''
    dateKey = ''
    try:
        opts, args = getopt.getopt(argv, "he:c:d:o:")
    except getopt.GetoptError:
        printusage()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            printusage()
            sys.exit()
        elif opt == '-e':
            inputfile = "env." + arg.strip() + ".properties"
        elif opt == '-c':
            configPath = arg.strip()
        elif opt == '-d':
            dateKey = arg.strip()
        elif opt == '-o':
            outputfile = arg.strip() + ".properties"
        else :
            print 'Invalid cmdline argument:',arg
            printusage()
            sys.exit(2)
    inputfile = os.path.join(configPath,inputfile)
    outputfile = os.path.join(configPath,outputfile)
    return (inputfile, dateKey, outputfile)


#Read the entire data of the file
def readfile(inputfile):
    print 'opening file :',inputfile
    inputstring = ''
    with open(inputfile,'r') as jsonfile:
        inputstring = jsonfile.read()
        print 'read String is: \n',inputstring
        print '\n end of read string'
    return inputstring

def getkeyname(prefix,key):
    if len(prefix) == 0:
        name = key
    else :
        name = prefix + "." + key
    return name


def getdatestring():
    return datetime.date.today().strftime("%d-%b-%Y")


def writefile(outputfile, data):
    with open(outputfile,"w") as fo:
        fo.write(data)


def main(argv):
    (inputfile, dateKey, outputfile) = getargs(argv)
    print 'input file is:',inputfile
    print 'date key is:',dateKey
    print 'output path is:', outputfile
    inputstring = readfile(inputfile)
    datevalue = getdatestring()
    data = inputstring + "\n" + dateKey + " = " + datevalue
    writefile(outputfile,data)


if __name__ == "__main__":
    main(sys.argv[1:])

