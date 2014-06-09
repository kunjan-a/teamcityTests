#!/usr/bin/python
import sys
import getopt
import os
import json
import types

#Print help for the cmdline usage
def printusage():
  print 'Usage:'
  print 'configGenerator.py -i <inputJsonFile> -o <outputPath>'
  print 'The paths should be relative to the current working directory.'
  print 'The inputJsonFile should contain a JOSNArray `environment`, listing all the environments for' \
        ' which properties files are to be generated.'
  print 'Also, it should have a JSONObject `config` that contains configuration fields with which the' \
        ' properties file will be populated.'
  print 'Inside the `config` JSONObject, a property that is same in all environments can be specified' \
        ' directly.\n A property whose value depends on the `environment` needs to specify a `default`' \
        ' value and `environment` specific value.\n If value is not provided specific to some ' \
        'environment then the `default` value will be used for that environment.'

  print '\n*******************************************\ne.g. for go.to run this command from gandalf:\n' \
        '  ./scripts/config_generator.py -i app/assets/config/config.js -o app/assets/config'


#Fetch the cmdline args and exit in case of improper usage
def getargs(argv):
  if len(argv) < 4:
    printusage()
    sys.exit(2)
  inputfile = ''
  outputpath = ''
  try:
    opts, args = getopt.getopt(argv, "hi:o:")
  except getopt.GetoptError:
    printusage()
    sys.exit(2)
  for opt, arg in opts:
    if opt == '-h':
      printusage()
      sys.exit()
    elif opt == '-i':
      inputfile = arg
    elif opt == '-o':
      outputpath = arg
    else :
      print 'Invalid cmdline argument:',arg
      printusage()
      sys.exit(2)
  inputfile = inputfile.strip()
  outputpath = outputpath.strip()
  return (inputfile, outputpath)


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


#Store key value pair for env in the config dictionary
def storeconfig(configs,env,key,value):
  print "storing in env:%s, key:%s, value:%s" % (env, key, value)
  configs[env][key] = value


#Populate the config for all the environments
def createconfig(name, key, value, configs, environments):
  if (key in environments) and (not(isinstance(value,types.DictType))):
    storeconfig(configs,key,name,value)
  elif isinstance(value,types.DictType):
    name1 = getkeyname(name,key)
    for (key1, value1) in value.items():
      createconfig(name1, key1, value1, configs, environments)
  else :
    storeconfig(configs,'default',getkeyname(name,key),value)


#Write a key value pair to the properties file object passed
def addpropertytofile(fileobject,key,value):
  finalvalue = json.dumps(value)
  if isinstance(value,types.StringType) or isinstance(value,types.UnicodeType):
    finalvalue = value
  fileobject.write("%s = %s\n" % (key,finalvalue))

def writeconfigfiles(configs,outputpath):
  defaultconfig = configs['default']
  del configs['default']
  filepath = os.path.join(outputpath,"common.properties")
  print "writing config file:",filepath
  with open(filepath,"w") as fo:
    fo.write("#Dont modify this file. Its auto-generated by config_generator.py\n")
    for key in sorted(defaultconfig.iterkeys()):
      addpropertytofile(fo,key,defaultconfig[key])

  for (env, config) in configs.items():
    filepath = os.path.join(outputpath,"env."+env+".properties")
    print "writing config file:",filepath
    with open(filepath,"w") as fo:
      fo.write("#Dont modify this file. Its auto-generated by config_generator.\n")
      for key in sorted(config.iterkeys()):
        addpropertytofile(fo,key,config[key])
      fo.write("\n\n#Following properties have been inherited from common.properties\n")
      for key in sorted(defaultconfig.iterkeys()):
        if not(config.has_key(key)):
          addpropertytofile(fo,key,defaultconfig[key])


#Process the config and create configs for respective environments
def process(inputjson):
  #print 'processing \n',inputjson
  environments = inputjson['environments']
  print 'environment:',environments
  environments.append('default')
  configs = {}
  for env in environments:
    configs[env] = {}
  config = inputjson['config']
  index = 0
  for (key, value) in config.items():
    print "item %d - %s:%s" % (index,key,value)
    createconfig("",key,value,configs,environments)
    index = index+1
  print "*********All storage is over*********"
  for (env,values) in configs.items():
    print "properties inside env:",env
    index = 0
    for (key, value) in values.items():
      print "%s = %s" % (key,value)
      index = index + 1
    print "-----------------"
  return configs


def main(argv):
  (inputfile, outputpath) = getargs(argv)
  print 'input file is:',inputfile
  print 'output path is:', outputpath
  inputstring = readfile(inputfile)
  try:
    inputjson = json.loads(inputstring)
  except ValueError as err:
    print("Error in parsing config file:"+inputfile+":",err)
    sys.exit(2)
  configs = process(inputjson)
  writeconfigfiles(configs,outputpath)


if __name__ == "__main__":
  main(sys.argv[1:])
