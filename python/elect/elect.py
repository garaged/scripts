#!/user/bin/env python
import argparse
import ConfigParser
from random import *
import math
import sys


def parseArgs():
  """
  Returns:
    array of CLI options
  """

  parser = argparse.ArgumentParser(description='voting simulator')
  parser.add_argument('-f', '--file', dest='filename', default=None,
      help='Reads a file to parse.', required=True)
  parser.add_argument('-s', '--style', dest='style', default='total',
      help='output style: total, percent. Default is total.', required=False, choices=['total', 'percent'])
  return parser.parse_args()

def Count(args):
  global Config
  part = {}
  set = {}
  Config = ConfigParser.ConfigParser()
  Config.read(args.filename)
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
  List = {}
  for k in part.keys():
    head += "{0},".format(k)
    List[k] = []
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
        List[k].insert(len(List[k]),int(part[k]['votes']))
        if args.style == 'total':
          out += "{0},".format(part[k]['votes'])
        elif args.style == 'percent':
          out += "{0},".format(100*(float( part[k]['votes']) / tot ))
      count = 0
      if x > 10:
        p = pearson(List['PRD'], List['PRI'])
        out += "{0},".format(p)
      print out

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


def pearson(X,Y):
  if len(X) != len(Y):
    print "none matching lists"
    #print len(X), len(Y)
  X_s = 0
  Y_s = 0
  # get averages
  for i in range(len(X)):
    X_s += X[i]
    Y_s += Y[i]
  X_a = X_s/len(X)
  Y_a = Y_s/len(Y)
  C=0
  X_2 = 0
  Y_2 = 0
  for i in range(len(X)):
    # Convariance
    C += (X[i]-X_a)*(Y[i]-Y_a)
    # Squares
    X_2 += (X[i]-X_a)**2
    Y_2 += (Y[i]-Y_a)**2

  P = 0
  if X_2 * Y_2 > 0:
    P = C/(math.sqrt(X_2)*math.sqrt(Y_2))
  return P

def main():
  args = parseArgs()
  Count(args)

if __name__ == '__main__':
  main();
