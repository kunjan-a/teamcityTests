#!/usr/bin/python
import sys
import getopt
import os
import commands
from xml.dom.minidom import parse


# Print help for the cmdline usage
def printusage():
    print 'Usage:'
    print 'versionSetter.py -m <inputAndroidManifestFile> -t <type>'
    print 'This cmd should be run from within the git repository.'
    print 'The paths should be relative to the current working directory.'
    print 'The inputAndroidManifestFile should contain xml elements `android:versionName` and `android:versionCode`.'
    print 'The type can be `market` or something else.'
    print '\n*******************************************\n' \
          'e.g. for go.to run this command from gandalf/:\n' \
          '  ./scripts/versionSetter.py -m app/AndroidManifest.xml -t market'


#Fetch the cmdline args and exit in case of improper usage
def getargs(argv):
    if len(argv) < 4:
        printusage()
        sys.exit(2)
    manifestfile = ''
    buildtype = 'dev'
    try:
        opts, args = getopt.getopt(argv, "hm:t:")
    except getopt.GetoptError:
        printusage()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            printusage()
            sys.exit()
        elif opt == '-m':
            manifestfile = arg
        elif opt == '-t':
            buildtype = arg
        else:
            print 'Invalid cmdline argument:', arg
            printusage()
            sys.exit(2)
    manifestfile = manifestfile.strip()
    buildtype = buildtype.strip()
    return (manifestfile, buildtype)


#Update the manifest file with the correct version name and code
def updatemanifest(manifestfile, versionname, versioncode):
    dom1 = parse(manifestfile)
    dom1.documentElement.setAttribute("android:versionName", versionname)
    dom1.documentElement.setAttribute("android:versionCode", versioncode)
    f = os.open(manifestfile, os.O_RDWR)
    os.ftruncate(f,0);
    os.write(f, dom1.toxml())


def runonshell(shellcmd):
    (status, tagdescription) = commands.getstatusoutput(shellcmd)
    if status != 0:
        print "error status:%s returned from cmd:%s" % (status, shellcmd)
        sys.exit(2)
    return status, tagdescription


def getversioncode():
    commitcountcmd = 'git rev-list HEAD --count'
    (status, versioncode) = commands.getstatusoutput(commitcountcmd)
    versioncode = versioncode.strip()
    print "git commit count gave status %s, versionCode %s" % (status, versioncode)
    return versioncode


def getversionname(buildtype, versioncode):
    versionname = ''
    describecmd = 'git describe --tags --match "v[0-9]*" --long'
    status, tagdescription = runonshell(describecmd)
    print "git describe tag gave status %s, tagdescription %s" % (status, tagdescription)
    tagdescription = tagdescription.strip()
    parts = tagdescription.split('-')
    print "description parts:", parts
    count = len(parts)
    prefix = parts[0:count - 2]
    print "description prefix:", prefix
    suffix = parts[count - 2] + "-" + parts[count - 1]
    print "description suffix:", suffix
    tag = "-".join(prefix)
    print "Latest market tag is:", tag

    versionname = tag + "." + versioncode

    if buildtype != 'market':
        versionname = versionname + "-" + suffix + "-" + buildtype

    return versionname


def main(argv):
    (manifestfile, buildtype) = getargs(argv)
    print 'manifest file is:', manifestfile
    print 'build type is:', buildtype
    versioncode = getversioncode()
    print "versioncode:", versioncode
    versionname = getversionname(buildtype, versioncode)
    print "versionname:", versionname
    updatemanifest(manifestfile, versionname, versioncode)


if __name__ == "__main__":
    main(sys.argv[1:])
