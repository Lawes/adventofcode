
import argparse
import os
import sys
import logging
import requests

# You must fill in SESSION following the instructions below.

# You can find SESSION:
# 1) Connect to https://adventofcode.com/2022/day/1/input
# 2) Find cookies with debug tools
# 3) Grab the value for session and copy to 'aoc_session' file. Fill it in.

argd = argparse.ArgumentParser()
argd.add_argument('year', type=int)
argd.add_argument('day', type=int)
argd.add_argument('-v', '--verbose', action='store_true')
args = argd.parse_args()

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG if args.verbose else logging.INFO)

logging.info('Load AOC cookie session')
with open('aoc_session', 'r') as f:
    SESSION = f.read()

url = f'https://adventofcode.com/{args.year}/day/{args.day}/input'
logging.info('Get url %s', url)

r = requests.get(url, cookies={'session': SESSION})
logging.info('Status code %s', r.status_code)
content = r.text.rstrip()
logging.info('Content size %s', len(content))
logging.debug('Content:\n%s', content)

filename = os.path.join(os.path.dirname(__file__), str(args.year), f'day{args.day:02}')
logging.info('Input directory=\'%s\'', filename)
os.makedirs(filename, exist_ok=True)

filename = os.path.join(filename, 'input')
logging.info('Write %s', filename)
with open(filename, 'w') as f:
    f.write(content)
