#key=61a82688e26edda8dd53da6cfe388253
#token=4b904a18f0346b5fb44b1818bf0cf5ea9e8d1d3f573f527657ca9635fc791016

import argparse

parser = argparse.ArgumentParser()

parser.add_argument("key", help="Your trello api key")
parser.add_argument("token", help="Your trello api token")
parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true") # action="count", default=False

args = parser.parse_args()
