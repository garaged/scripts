#!/user/bin/env python
import argparse
import ConfigParser
from random import *
import sys


def parseArgs():
  """
  Returns:
    array of CLI options
  """

  parser = argparse.ArgumentParser(description='voting simulator')
  parser.add_argument('-f', '--file', dest='filename', default=None,
      help='Reads a file to parse.', required=True)
  return parser.parse_args()

def Count(file):
  global Config
  part = {}
  set = {}
  Config = ConfigParser.ConfigParser()
  Config.read(file)
  parties = Config.sections()
  for item in parties:
    part[item] = ConfigSectionMap(item)
  main = part['main']
  del part['main']
  sum = 0
  for k in part.keys():
    sum += float(part[k]['percent'])
  tmp = 1 - sum
  part['ABS'] = {}
  part['ABS']['percent'] = str(tmp)
  part['ABS']['votes'] = 0
  tmp = 0
  for k in part.keys():
    cur = float(part[k]['percent'])
    set[k] = tmp + cur
    tmp += cur
    count = 0
    tot = 0
  head = 'step,'
  for k in part.keys():
    head += "{0},".format(k)
  print head
  for x in xrange(int(main['loops'])):
    count += 1
    tot += 1
    rnd = rand_elect()
    for k in set.keys():
      if rnd < float(set[k]):
        part[k]['votes'] = int(part[k]['votes']) + 1
        break
    if ( count >= int(main['cnt']) ):
      out = `tot/float(main['loops'])`+","
      for k in part.keys():
        #out += "{0},".format(100*(float( part[k]['votes']) / tot ))
        out += "{0},".format(part[k]['votes'])
      print out
      count = 0
  #print part

def ConfigSectionMap(section):
  dict1 = {}
  options = Config.options(section)
  for option in options:
    try:
      dict1[option] = Config.get(section, option)
      if dict1[option] == -1:
        DebugPrint("skip: %s" % option)
    except:
      print("exception on %s!" % option)
      dict1[option] = None
  return dict1


def rand_elect():
  return random()


def main():
  args = parseArgs()
  Count(args.filename)

if __name__ == '__main__':
  main();
